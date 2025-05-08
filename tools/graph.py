"""Main graph for the writing assistant."""

from typing import Literal, TypedDict, cast

from langgraph.graph import END, START, StateGraph

from tools.config import load_chat_model
from tools.state import WritingState


async def analyze_content(state: WritingState) -> dict[str, str]:
    """Analyze the content and extract the behavior type and prompt."""
    if state.behavior:
        print(f"直接下一个，此时的行为：{state.behavior}")
        return {"behavior": state.behavior, "prompt": state.content}
    content_lines = state.content.strip().split('\n')
    if not content_lines:
        return {"behavior": "topic", "content": ""}

    last_line = content_lines[-1].strip().lower()
    print(f"最后一行:{last_line}")
    prompt = '\n'.join(content_lines[:-1]).strip()
    print(f"prompt:{prompt}")

    if last_line == "topic":
        return {"behavior": "topic", "content": prompt}
    elif last_line == "rewrite":
        return {"behavior": "rewrite", "content": prompt}
    elif last_line == "generate":
        return {"behavior": "generate", "content": prompt}
    elif last_line == "cite":
        return {"behavior": "cite", "content": prompt}
    else:
        return {"behavior": "topic", "content": state.content}


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
         "content": "You are a professional English writer. Write a concise and engaging introduction paragraph for the given topic. Keep it under 100 words."},
        {"role": "user", "content": f"Topic: {state.content}"}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def rewrite_content(state: WritingState) -> dict[str, str]:
    """Rewrite the content to improve its quality without adding new content."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "You are a professional English editor. Improve the writing quality of the given text without adding new content or changing the meaning. Focus on grammar, word choice, and sentence structure."},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def generate_content(state: WritingState) -> dict[str, str]:
    """Generate 1-2 lines of content based on the given text."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": "You are a professional English writer. Add 1-2 lines of content that naturally follows the given text. Keep it concise and relevant."},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


async def cite_content(state: WritingState) -> dict[str, str]:
    """Paraphrase the content and add Harvard style citation."""
    model = load_chat_model()
    messages = [
        {"role": "system",
         "content": """You are a professional academic writer. Your task is to:
            1. Paraphrase the given text in your own words while maintaining the original meaning
            2. Add a Harvard style citation at the end of the paraphrased text
            3. Keep the paraphrased text concise and clear
            4. Format the citation as: (Author's Last Name, Year)"""},
        {"role": "user", "content": state.content}
    ]
    response = await model.ainvoke(messages)
    return {"response": response.content}


# Define the graph
builder = StateGraph(WritingState)
builder.add_node("analyze_content", analyze_content)
builder.add_node("write_introduction", write_introduction)
builder.add_node("rewrite_content", rewrite_content)
builder.add_node("generate_content", generate_content)
builder.add_node("cite_content", cite_content)

# Add edges
builder.add_edge(START, "analyze_content")
builder.add_conditional_edges(
    "analyze_content",
    route_behavior,
    {
        "write_introduction": "write_introduction",
        "rewrite_content": "rewrite_content",
        "generate_content": "generate_content",
        "cite_content": "cite_content"
    }
)
builder.add_edge("write_introduction", END)
builder.add_edge("rewrite_content", END)
builder.add_edge("generate_content", END)
builder.add_edge("cite_content", END)

# Compile the graph
graph = builder.compile()