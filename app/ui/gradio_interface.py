import asyncio
from typing import Tuple

import gradio as gr

from ..services.agents.langgraph_agent import LangGraphAgent


class GradioInterface:
    """Gradio interface for the agent system"""

    def __init__(self):
        self.agent = LangGraphAgent()
        self.initialized = False

    async def initialize_agent(self):
        """Initialize the agent"""
        if not self.initialized:
            await self.agent.initialize()
            self.initialized = True

    async def chat_with_agent(
        self, message: str, history, model_name: str
    ) -> Tuple[str, list]:
        """Handle chat with the agent"""
        await self.initialize_agent()

        # Switch model if needed
        await self.agent.switch_model(model_name)

        # Process the message
        response = await self.agent.chat(message)

        # Update history
        if history is None:
            history = []

        history.append([message, response])

        return "", history

    async def get_available_models(self) -> list:
        """Get available models"""
        return await self.agent.get_available_models()

    def create_interface(self):
        """Create the Gradio interface"""
        with gr.Blocks(
            title="Alpha Agents - Visa Checker & Browser Automation"
        ) as interface:
            gr.Markdown("# 🤖 Alpha Agents - Advanced AI Assistant")
            gr.Markdown(
                """
            This agent can help you with:
            - 🌐 **Browser automation** (navigate, extract content,
              interact with websites)
            - 🇮🇳 **Visa slot checking** (monitor Indian embassy visa availability)
            - 📱 **Push notifications** (send alerts to your device)
            - 🔄 **Model switching** (use different AI models for different tasks)
            """
            )

            with gr.Row():
                with gr.Column(scale=3):
                    # Chat interface
                    chatbot = gr.Chatbot(
                        height=500, label="Chat with Agent", show_label=True
                    )

                    with gr.Row():
                        msg = gr.Textbox(
                            placeholder="Ask me to check visa slots \
                                 or browse websites...",
                            label="Message",
                            scale=4,
                        )
                        submit_btn = gr.Button("Send", scale=1, variant="primary")

                with gr.Column(scale=1):
                    # Model selection
                    model_dropdown = gr.Dropdown(
                        choices=["OpenRouter - Claude 3.5 Sonnet"],  # Will be updated
                        value="OpenRouter - Claude 3.5 Sonnet",
                        label="🤖 Select AI Model",
                        interactive=True,
                    )

                    gr.Markdown("### 🛠️ Quick Actions")

                    quick_visa_btn = gr.Button(
                        "🔍 Check Visa Slots", variant="secondary"
                    )
                    quick_browse_btn = gr.Button("🌐 Browse CNN", variant="secondary")
                    quick_screenshot_btn = gr.Button(
                        "📸 Take Screenshot", variant="secondary"
                    )
                    quick_notify_btn = gr.Button(
                        "📱 Send Test Notification", variant="secondary"
                    )

                    gr.Markdown("### 📋 Available Tools")
                    gr.Markdown(
                        """
                    - **Browser Tools**: Navigate, extract text, take screenshots
                    - **Visa Checker**: Monitor Indian embassy visa slots
                    - **Notifications**: Send push alerts via Pushover
                    """
                    )

            # Event handlers
            def handle_submit(message: str, history, model: str):
                if not message.strip():
                    return "", history

                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    new_msg, new_history = loop.run_until_complete(
                        self.chat_with_agent(message, history, model)
                    )
                    return new_msg, new_history
                finally:
                    loop.close()

            def handle_quick_visa(history, model: str):
                return handle_submit(
                    "Check visa slot availability on the Indian embassy website",
                    history,
                    model,
                )

            def handle_quick_browse(history, model: str):
                return handle_submit(
                    "Navigate to https://www.cnn.com and extract the main headlines",
                    history,
                    model,
                )

            def handle_quick_screenshot(history, model: str):
                return handle_submit(
                    "Take a screenshot of the current page", history, model
                )

            def handle_quick_notify(history, model: str):
                return handle_submit(
                    "Send me a test push notification \
                    saying 'Alpha Agents is working!'",
                    history,
                    model,
                )

            # Bind events
            submit_btn.click(
                handle_submit,
                inputs=[msg, chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            msg.submit(
                handle_submit,
                inputs=[msg, chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            quick_visa_btn.click(
                handle_quick_visa,
                inputs=[chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            quick_browse_btn.click(
                handle_quick_browse,
                inputs=[chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            quick_screenshot_btn.click(
                handle_quick_screenshot,
                inputs=[chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            quick_notify_btn.click(
                handle_quick_notify,
                inputs=[chatbot, model_dropdown],
                outputs=[msg, chatbot],
            )

            # Load available models on startup
            def load_models():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    models = loop.run_until_complete(self.get_available_models())
                    return gr.Dropdown(
                        choices=models, value=models[0] if models else None
                    )
                finally:
                    loop.close()

            interface.load(load_models, outputs=[model_dropdown])

        return interface

    async def launch(self, share: bool = False, server_port: int = 7860):
        """Launch the Gradio interface"""
        interface = self.create_interface()

        try:
            interface.launch(share=share, server_port=server_port, show_error=True)
        except Exception as e:
            print(f"Error launching Gradio interface: {e}")
            raise
