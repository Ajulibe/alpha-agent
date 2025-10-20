from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.models.state import State
from app.services.llm_service import LLMService
from app.services.tools.browser_tools import BrowserToolsService
from app.services.tools.notification_tool import notification_tool
from app.services.tools.screenshot_tool import screenshot_tool
from app.services.tools.visa_tool import visa_check_tool


class LangGraphAgent:
    """Main LangGraph agent service"""

    def __init__(self):
        self.llm_service = LLMService()
        self.browser_service = BrowserToolsService()
        self.graph = None
        self.current_model = None
        self.tools = []

    async def initialize(self, model_name: str = "OpenRouter - Claude 3.5 Sonnet"):
        """Initialize the agent with a specific model"""
        self.current_model = model_name
        llm = self.llm_service.get_model(model_name)

        # Initialize browser tools
        browser_tools = await self.browser_service.get_tools()

        # Combine all tools
        self.tools = [
            visa_check_tool,
            notification_tool,
            screenshot_tool,
        ] + browser_tools

        # Bind tools to LLM
        llm_with_tools = llm.bind_tools(self.tools)

        # Build the graph
        graph_builder = StateGraph(State)

        # Add chatbot node
        def chatbot(state: State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # Add edges
        graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")

        # Compile with memory
        memory = MemorySaver()
        self.graph = graph_builder.compile(checkpointer=memory)

    async def switch_model(self, model_name: str):
        """Switch to a different model"""
        if model_name != self.current_model:
            await self.initialize(model_name)

    async def chat(self, message: str, thread_id: str = "default") -> str:
        """Process a chat message"""
        if not self.graph:
            await self.initialize()

        config = {"configurable": {"thread_id": thread_id}}

        try:
            result = await self.graph.ainvoke(
                {"messages": [{"role": "user", "content": message}]}, config=config
            )
            return result["messages"][-1].content
        except (ValueError, RuntimeError, ImportError, KeyError) as e:
            return f"❌ Error processing message: {str(e)}"

    async def get_available_models(self) -> list:
        """Get list of available models"""
        return self.llm_service.get_available_models()

    async def close(self):
        """Clean up resources"""
        await self.browser_service.close()
