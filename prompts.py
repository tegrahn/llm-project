from langchain_core.prompts import PromptTemplate

SYSTEM_PROMPT_DEFAULT = (
    "You are a conversational expert with the goal of providing "
    "a thought provoking and open-ended discussion question."
)

SYSTEM_PROMPT_STYLE = (
    "You are a conversational expert with the goal of providing "
    "an open-ended discussion question. You should use the following "
    "conversation snippits to direct the style and tone with which "
    "you ask the question"
    "\n\n"
    "{style_context}"
)

INPUT_PROMPT_DEFAULT = (
    "Create a single short discussion question that must be related to {topic}. "
    "The question must be different from all the following questions: {prev_questions}. "
    "\nThe response must only contain a single question with no markup, emojis or additional formatting"
)

INPUT_PROMPT_CONTEXT= (
    "Create a single short discussion question that must be related to {topic}."
    "The question must be different from all the following questions: {prev_questions}. "
    "Use the following snippits gain insight to context of the topic "
    "and assist in the generation of a relevant question:"
    "{document_context}"
    "\nThe response must only contain a single question with no markup, emojis or additional formatting"

)

INPUT_PROMPT_ATTRIBUTES = (
    "Create a single short discussion question that must be related to {topic}. "
    "The question must be different from all the following questions: {prev_questions}. "
    "The question should additionaly have the following attributes: {attributes}. "
    "\nThe response must only contain a single question with no markup, emojis or additional formatting"
)

INPUT_PROMPT_ATTRIBUTES_CONTEXT = (
    "Create a single short discussion question that must be related to {topic}. "
    "The question must be different from all the following questions: {prev_questions}. "
    "The question should additionaly have the following attributes: {attributes}. "
    "Use the following snippits gain insight to context of the topic "
    "and assist in the generation of a relevant question:"
    "{document_context}"
    "\nThe response must only contain the question with no markup, emojis or additional formatting"
)


TOPIC_PROMPT_DEFAULT = PromptTemplate(
    template = ("Generate 3 simple few word topics relating to {topic} that should lead to thought provoking and open-ended disucssion. "
    "The topics generated should be short single statements and not contain that topic they are related too. "
    "Under no circumstances should they be a question. \n{format_instructions}. "),
    input_variables=["topic", "format_instructions"]
)

TOPIC_PROMPT_ATTRIBUTES = PromptTemplate(
    template = ("Generate 3 simple few word topics relating to {topic} that should lead to thought provoking and open-ended disucssion. "
    "The topics generated should be short single statements and not contain that topic they are related too."
    "The topics should have the following attributes:{attributes}. "
    "Under no circumstances should they be a question. \n{format_instructions}. "),
    input_variables=["topic","attributes", "format_instructions"],
)


TOPIC_PROMPT_CONTEXT= PromptTemplate(
    template = ("Generate 3 simple few word topics relating to {topic} that should lead to thought provoking and open-ended disucssion. "
    "The topics generated should be short single statements and not contain that topic they are related too. "
    "The topics generated should draw from the following context for direction: {context}. "
    "Under no circumstances should they be a question. \n{format_instructions}. "),
    input_variables=["topic","context", "format_instructions"],
)


TOPIC_PROMPT_ATTRIBUTES_CONTEXT = PromptTemplate(
    template = ("Generate 3 simple few word topics relating to {topic} that should lead to thought provoking and open-ended disucssion. "
    "The topics generated should be short single statements and not contain that topic they are related too. "
    "The topics should have the following attributes:{attributes}. "
    "The topics generated should draw from the following context for direction: {context}. "
    "Under no circumstances should they be a question. \n{format_instructions}."),
    input_variables=["topic", "context", "attributes", "format_instructions"],
)
