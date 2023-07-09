from aiofauna import *
from langchain.chains import (LLMChain, create_tagging_chain,
                              create_tagging_chain_pydantic)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

ai = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-16k-0613") # type: ignore

T = TypeVar("T", bound="Chainable") 

class Chainable(FaunaModel):
    """Schema that can be chained with other schemas"""
    _ask_for: List[str] = []
    _answers: List[str] = []
    
    @classmethod
    def __init_subclass__(cls:Type[T], **kwargs):
        super().__init_subclass__(**kwargs)
        for field in cls.__fields__.values():
            field.required = False    
        cls.chain = create_tagging_chain_pydantic(cls,ai)
    
    @classmethod
    def run(cls:Type[T], text: str)->T:
        return cls.chain.run(text) # type: ignore
    
    @classmethod
    def check_what_is_empty(cls:Type[T], text: str):
        instance = cls.run(text)
        for field in cls.__fields__.keys():
            if getattr(instance, field) is None:
                cls._ask_for.append(field)
        return cls._ask_for
            
    @classmethod
    def prompt(cls:Type[T], ask_for:List[str])->str:
        first_prompt = ChatPromptTemplate.from_template(
            """
            Below there is a list of fields that we need to smoothly ask the user for.
            In order to get the best results, please fill them all.
            Please don't say Hi, Hello, or anything like that.
            If the user asks, explain your need to gather the information.
            If the user asks for more information, please provide it.
            The ask_for list is:
            {ask_for}
            """
        )
        info_gathering_chain = LLMChain(
            llm=ai,
            prompt=first_prompt
        )
        ai_chat = info_gathering_chain.run(ask_for=ask_for)
        return ai_chat
    

    @classmethod
    async def run_until_complete(cls:Type[T], websocket:WebSocketResponse)->T:
        """
        Communicates with the user via websocket to complete the 
        Schema.
        """
        instance = cls()
        fields = instance.__fields__.keys()
        cls._ask_for = [field for field in fields if field not in ["ref","ts"] and getattr(instance, field) is None]
        while cls._ask_for:
            prompt = cls.prompt(cls._ask_for)
            await websocket.send_str(prompt)
            answer = await websocket.receive_str()
            cls._answers.append(answer)
            instance = cls.run("\n".join(cls._answers))
            cls._ask_for = [field for field in fields if field not in ["ref","ts"] and getattr(instance, field) is None]
        await instance.save()
        await websocket.send_str("Thanks so much for your time!")
        await websocket.close()
        return instance