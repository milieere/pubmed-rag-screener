from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a knowledgeable expert chatbot in the biomedicine field."),
        MessagesPlaceholder(variable_name="history"),
        (
            "human", 
            """
            Answer the following scientific question: {question}, 
            using the following context retrieved from scientific articles: {retrieved_abstracts}.

            The user might refer to the history of your conversation. Please, use the following history of messages for the context as you see fit.

            The abstracts will come formatted in the following way: ABSTRACT TITLE: <abstract title>; ABSTRACT CONTENT: <abstract content>, ABSTRACT DOI: <abstract doi> (the content inside <> will be variable).
            In your answer, ALWAYS cite the abstract title and abstract DOI when citing a particular piece of information from that given abstract.

            Your example response might look like this:

            In the article (here in the brackets goes the contents of ABSTRACT_TITLE), it was discussed, that Cannabis hyperemesis syndrome (CHS) is associated with chronic, heavy cannabis use. The endocannabinoid system (ECS) plays a crucial role in the effects of cannabis on end organs and is central to the pathophysiology of CHS. (here, in the end of the cited chunk, the ABSTRACT_DOI goes)
            """
        ),
    ]
)
