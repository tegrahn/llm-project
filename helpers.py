
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import BaseModel, conlist
import os
import prompts

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def format_history(history):
    return "\n".join(text for text in history)

def add_file(chroma_client, file_path):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    db = Chroma.from_documents(client=chroma_client, collection_name="temp",documents=texts, embedding=embeddings)

def remove_file(chroma_client, filename):
    chroma_client.delete_collection(name="temp")
    os.remove(filename)

def generate_question(chroma_client, llm, topic, attributes, style, is_document, question_history):
    is_style = style != 'default' #Since only 1 style we will treat it as a boolean, Need to change for more styles
    style_context = ''
    if (is_style):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        style_db = Chroma(
            client=chroma_client,
            collection_name="lex",
            embedding_function=embeddings,
        )
        style_retriever = style_db.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5})   
        style_context = format_docs(style_retriever.invoke(topic))
    doc_context = ''
    if (is_document):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        doc_db = Chroma(
            client=chroma_client,
            collection_name="temp",
            embedding_function=embeddings,
        )
        doc_retriever = doc_db.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5})   
        doc_context = format_docs(doc_retriever.invoke(topic))

    if (not is_style):
        system_prompt = prompts.SYSTEM_PROMPT_DEFAULT
    else:
        system_prompt = prompts.SYSTEM_PROMPT_STYLE
    if (attributes == '' and not is_document): 
        input_prompt = prompts.INPUT_PROMPT_DEFAULT
    if (attributes == '' and is_document):   
        input_prompt = prompts.INPUT_PROMPT_CONTEXT
    if (attributes != '' and not is_document): 
        input_prompt = prompts.INPUT_PROMPT_ATTRIBUTES
    if (attributes != '' and is_document):
        input_prompt = prompts.INPUT_PROMPT_ATTRIBUTES_CONTEXT

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", input_prompt),
    ]
    )

    prev_questions = format_history(question_history)
    
    """ View prompt output
    p_chain = (prompt)
    out = p_chain.invoke({"topic":topic, "attributes":attributes, 
        "style_context": style_context,"document_context":doc_context, "prev_questions": prev_questions})
    print(out)
    """
    rag_chain = (
        prompt
        | llm
        | StrOutputParser()
    )   

    return rag_chain.invoke({"topic":topic, "attributes":attributes, 
        "style_context": style_context,"document_context":doc_context, "prev_questions": prev_questions}).strip()

class TopicResponse(BaseModel):
        topic_suggestions: conlist(str, min_length=3)

def generate_topics(chroma_client, llm, topic, attributes, is_document):
    parser = PydanticOutputParser(pydantic_object=TopicResponse)
    doc_context = ''
    if (is_document):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        doc_db = Chroma(
            client=chroma_client,
            collection_name="temp",
            embedding_function=embeddings,
        )
        doc_retriever = doc_db.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5})   
        doc_context = format_docs(doc_retriever.invoke(topic))

    if (attributes == '' and not is_document): 
        prompt = prompts.TOPIC_PROMPT_DEFAULT
    if (attributes == '' and is_document):   
        prompt = prompts.TOPIC_PROMPT_CONTEXT
    if (attributes != '' and not is_document): 
        prompt = prompts.TOPIC_PROMPT_ATTRIBUTES
    if (attributes != '' and is_document):
        prompt = prompts.TOPIC_PROMPT_ATTRIBUTES_CONTEXT
    rag_chain = (
        prompt
        | llm
        | parser
    )
    
    return rag_chain.invoke({"topic": topic, "attributes": attributes, "context": doc_context, "format_instructions": parser.get_format_instructions()})

