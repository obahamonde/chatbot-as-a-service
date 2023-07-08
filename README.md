OK now that you have all the context, let's get started!

The idea is the following:

What we have?
An infinite memoery engine for chatbots thanks to pinecone and openai
A mechanism to scrap and ingest data from any website with a sitemap.xml most websites are Wordpress based so this is a good start
A well defined models for a simple CRM Leads, Organizations, Users, Chatbots, etc
A way to deploy an application as a lambda function in AWS

What we want?
Multitenant Application that is a CRM lead generator powered by the chatbot engine
Personalization of the ContextTemplate to inject into bot windows
Deploy the chatbot to aws using fastapi and lambda function
Deploy a DB for each customer that will hold all their crm data
This way we have multitenancy, personalization, and infinite memory for the chatbots

