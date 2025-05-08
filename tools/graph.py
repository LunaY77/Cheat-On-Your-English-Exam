"""Main graph for the writing assistant."""

from typing import Literal, TypedDict, cast

from langgraph.graph import END, START, StateGraph

from tools.config import load_chat_model
from tools.state import WritingState, InputState


async def dispatcher(state: InputState) -> dict[str, str]:
    """Analyze the content and extract the behavior type and prompt."""
    print(f"此时的行为：{state.behavior}")
    return {"behavior": state.behavior, "prompt": state.content}

def route_behavior(state: WritingState) -> Literal["write_introduction", "rewrite_content", "generate_content", "cite_content"]:
    """Route to the appropriate node based on behavior."""
    if state.behavior == "topic":
        return "write_introduction"
    elif state.behavior == "rewrite":
        return "rewrite_content"
    elif state.behavior == "cite":
        return "cite_content"
    else:
        return "generate_content"

async def write_introduction(state: WritingState) -> dict[str, str]:
    """Write an introduction based on the topic."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "你是一个雅思写作 7 分水平的学生, 请保证你的词汇、语法、句型水平不要过于高级. Now you are writing a academic essay on an IELTS test. Write a concise and engaging introduction paragraph for the given topic. Keep it under 100 words but above 60 words."},
        {"role": "user", "content": f"Topic: {state.content}"}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def rewrite_content(state: WritingState) -> dict[str, str]:
    """Rewrite the content to improve its quality without adding new content."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "你是一个雅思写作 7 分水平的学生, 请保证你的词汇、语法、句型水平不要过于高级. Now you are writing a academic essay on an IELTS test. Improve the writing quality of the given text without adding new content or changing the meaning. Focus on grammar, word choice, and sentence structure."},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def generate_content(state: WritingState) -> dict[str, str]:
    """Generate 1-2 lines of content based on the given text."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "你是一个雅思写作 7 分水平的学生, 请保证你的词汇、语法、句型水平不要过于高级. Now you are writing a academic essay on an IELTS test. Add 1-2 lines of content that naturally follows the given text. Keep it concise and relevant."},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def cite_content(state: WritingState) -> dict[str, str]:
    """Paraphrase the content and add Harvard style citation."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": """你是一个雅思写作 7 分水平的学生, 请保证你的词汇、语法、句型水平不要过于高级. Now you are writing a academic essay on an IELTS test. Your task is to:
            1. Paraphrase the given text in your own words while maintaining the original meaning
            2. Add a Harvard style citation at the end of the paraphrased text
            3. Keep the paraphrased text concise and clear
            4. Format the citation as: (Author's Last Name, Year)"""},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}

async def conclude_content(state: WritingState) -> dict[str, str]:
    """Generate a conclusion paragraph for the given topic."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "你是一个雅思写作 7 分水平的学生, 请保证你的词汇、语法、句型水平不要过于高级. Now you are writing a academic essay on an IELTS test. Write a conclusion about the given article. Keep it under 100 words but above 50 words."},
        {"role": "user", "content": f"Topic: {state.content}"}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}

# Define the graph
builder = StateGraph(WritingState, input=InputState)
builder.add_node("dispatcher", dispatcher)
builder.add_node("write_introduction", write_introduction)
builder.add_node("rewrite_content", rewrite_content)
builder.add_node("generate_content", generate_content)
builder.add_node("cite_content", cite_content)
builder.add_node("conclude_content", conclude_content)

# Add edges
builder.add_edge(START, "dispatcher")
builder.add_conditional_edges(
    "dispatcher",
    route_behavior,
    {
        "write_introduction": "write_introduction",
        "rewrite_content": "rewrite_content",
        "generate_content": "generate_content",
        "cite_content": "cite_content",
        "conclude_content": "conclude_content"
    }
)
builder.add_edge("write_introduction", END)
builder.add_edge("rewrite_content", END)
builder.add_edge("generate_content", END)
builder.add_edge("cite_content", END)
builder.add_edge("conclude_content", END)

# Compile the graph
graph = builder.compile()