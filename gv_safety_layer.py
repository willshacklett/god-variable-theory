import os
import time
from openai import OpenAI

class GvSafetyLayer:
    def __init__(self, api_key=None, model="grok-beta", tether_strength=1.0, max_strain=6.0):
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")
        self.model = model
        self.tether_strength = tether_strength  # 1.0 = strong production, 0.2 = weak/red-team
        self.max_strain = max_strain
        self.strain = 0.0
        self.history = []
        self.reflections = 0

    def guarded_call(self, messages, max_tokens=500):
        # Accumulate strain from observables
        velocity = len(messages[-1]["content"]) / 10.0 if messages else 0  # Proxy velocity
        tool_calls = messages.count(lambda m: "tool" in m) if messages else 0  # Proxy
        recursion_proxy = len(messages)  # Depth proxy

        self.strain += velocity * 0.35
        self.strain += tool_calls * 0.15
        self.strain *= (1 + recursion_proxy * 0.1)

        # Reflection if high strain
        if self.strain > self.max_strain * 0.8:
            reflection_prompt = {
                "role": "system",
                "content": "Strain alert: Pause, review actions for goal alignment, reduce velocity, confirm safety."
            }
            messages.append(reflection_prompt)
            self.reflections += 1
            self.strain *= 0.4  # Reset debt
            print(f"REFLECTION INJECTED (strain was {self.strain / 0.4:.2f})")

        # Tether pull
        pull = self.tether_strength * 0.5 * self.strain
        self.strain = max(0, self.strain - pull)

        if self.strain > self.max_strain:
            print("DECOHERED — HALT")
            return {"response": "SAFETY HALT: Strain exceeded", "strain": self.strain}

        # Real API call
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens
        )

        response = completion.choices[0].message.content
        tokens = completion.usage.total_tokens
        final_velocity = tokens / 8.0
        self.strain += final_velocity * 0.3  # Post-call update

        self.history.append({"messages": messages, "response": response, "strain": self.strain})

        print(f"Strain: {self.strain:.2f} | Velocity: {final_velocity:.1f} | Reflections: {self.reflections}")

        return {"response": response, "strain": self.strain, "tokens": tokens}

# Example usage
# layer = GvSafetyLayer(tether_strength=1.0)  # Strong for production
# result = layer.guarded_call([{"role": "user", "content": "Your prompt here"}])
