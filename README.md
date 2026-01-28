<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

Welcome to the Stone Ridge Agent Engineering course!

**You can access everything you need to succeed in the course directly through this GitHub repo** Specifically, through [`00_Quicklinks`](00_AE_Quicklinks/README.md).

# 🛣️ Getting Started
To prepare for kicking off our training on Tuesday, January 27th at 5 PM ET [here](https://stoneridgeam.zoom.us/j/88996041038?pwd=5kqaGAUqkkAnCtqrwc11cPxSioCNcZ.1) (passcode: `133735`), be sure that you have the following things completed:

1. 📅 Follow the [course calendar](https://bit.ly/SRHG_AE_Training) for office hours and class links!
2. 🧑‍💻 Complete [The AI Engineer Challenge](https://aimakerspace.io/aie-challenge)
3. 🌡️ Fill out your [starting self-assessment](https://forms.gle/PmVj3GCDf9UqWCoCA)!
4. 🛹 Schedule your [Onboarding Call](https://calendly.com/aim-dr-greg/srhg-agent-engineering-training-with-ai-makerspace) with Dr. Greg!
5. 🤓 Prepare to hit the ground running in Week 1 by reading the information available now [`00_Docs`](00_Docs)

# 📅 Structure & Format

- Weekly content releases & tag-ups on Tuesdays from 5-6 PM ET
- 2 assignments per week
- 24-hour async Slack channel to be staffed to get responses *within the workday*

## 📚 Learning Outcomes

<details>
  <summary><strong>Week 1: Building & Vibe Checking Class RAG Applications</strong></summary>

  <ul>
    <li><em>✨ Intro &amp; Vibe Check</em>: Check the vibes on the LLM app you built during The AI Engineer Challenge and see how even naive context updates can have a big impact.</li>
    <li><em>🗃️ Dense Vector Retrieval</em>: Understand RAG from first principles, both conceptually and in code.</li>
  </ul>
</details>

<details>
  <summary><strong>Week 2: Building and Monitoring Agentic RAG Applications</strong></summary>

  <ul>
    <li><em>🔁 The Agent Loop</em>: Understand what an “agent” is and how to use the latest abstractions to build production-grade agents quickly.</li>
    <li><em>🕴️ Agentic RAG</em>: Look under the hood of agentic RAG and the <code>create_agent</code> abstraction.</li>
  </ul>
</details>

<details>
  <summary><strong>Week 3: Building More Complex Agentic Applications</strong></summary>

  <ul>
    <li><em>🔄 Multi-Agent Applications</em>: Learn when to add additional agents to optimize context and how to construct agent teams using common patterns.</li>
    <li><em>🧠 Agent Memory</em>: Learn how to build agents that manage both short- and long-term memory.</li>
  </ul>
</details>

<details>
  <summary><strong>Week 4: Systematic Evals for Agentic RAG Applications</strong></summary>

  <ul>
    <li><em>🧪 Synthetic Data Generation for Evals</em>: Learn how to automatically generate test data for agentic RAG applications when no eval datasets exist.</li>
    <li><em>📊 Agentic RAG Evaluation</em>: Set up and implement effective evals for agents and RAG applications.</li>
  </ul>
</details>

<details>
  <summary><strong>Week 5: Deeper on Agents &amp; RAG</strong></summary>

  <ul>
    <li><em>🐕 Advanced Retrievers</em>: Learn retrieval best practices and a systematic approach to choosing the right retriever for your AI applications.</li>
    <li><em>🔌 MCP Connectors</em>: Learn how to leverage collections of tools to enhance retrieval on the client side of MCP servers.</li>
    <li><em>📶 Deep Agents</em>: Build complex agents that operate over longer time horizons.</li>
    <li><em>🕵️ Deep Research</em>: Understand how deep research systems work under the hood and how to build them.</li>
  </ul>
</details>

<details>
  <summary><strong>Week 6: Agent Servers &amp; Production Upgrades</strong></summary>

  <ul>
    <li><em>🚢 Agent Servers</em>: Learn to deploy complex agent applications to production endpoints you can use elsewhere.</li>
    <li><em>🔀 MCP Servers</em>: Learn how to set up MCP servers and enable public communication between agents.</li>
    <li><em>🛤️ Guardrails &amp; Caching</em>: Learn practical upgrades for performance, security, and trustworthiness.</li>
  </ul>
</details>



# **🧰 Tooling**

We will work within the AWS ecosystem and within the Deployment Process used by your organization; e.g.,

<details>
<summary><strong>SRHG Deployment Process</strong></summary>

1. GitHub
2. Write code in a feature branch
3. PR with CODEOWNERS approval to merge into `main`
4. GitHub Actions on ephemeral ARC CI/CD runners to build, test, and deploy Docker images to AWS ECR
5. Terraform manages declarative infrastructure in AWS
6. ArgoCD watches the `main` branch  
   - Auto-sync enabled for low-risk changes  
   - Manual sync required for higher-risk changes
7. Datadog for metrics, monitoring, APM, and logging

</details>

Specifically, we will leverage the following tooling in the curriculum and assignments:

- **Hardware Requirements**: Apple Macbook Pro, M-Chip Series
- **Cloud Service Provider**: AWS
- **LLM & Embedding Model Serving & Inference**: Anthropic Models through AWS Bedrock
- **Version Control**: GitHub
- **Coding Agent:** Claude Code (running locally)
- **MCP Servers**: Office365 ChatGPT connector, AWS Knowledgebase for Confluence (specific spaces)
- **Agent Orchestration**: LangGraph
- **Monitoring, Observability, and Deployment**: LangSmith

# 🧑‍🤝‍🧑 Your Support Team

- [Dr. Greg Loughnane, Ph.D](https://www.linkedin.com/in/gregloughnane/), CEO & Co-Founder @ AI Makerspace
- [Chris Alexiuk](https://www.linkedin.com/in/csalexiuk/), CTO & Co-Founder @ AI Makerspace
- [Jacob Kilpatrick](https://www.linkedin.com/in/jacobkilpatrickai/), Course Operations Lead @ AI Makerspace
- [Dr. Katerina Gawthorpe, Ph.D.](https://www.linkedin.com/in/katerina-gawthorpe/), Co-Founder @ [eve.ai](http://eve.ai), AI Makerspace-Certified Consultant
- [Betsy Gold](https://www.linkedin.com/in/betsybgold/), Co-Founder @ [eve.ai](http://eve.ai), AI Makerspace-Certified Consultant
- [Mani Sarkar](https://www.linkedin.com/in/mani-sarkar/), 4X Kaggle Expert, Polyglot Engineer

# **🏆 Grading**

Each week, you will receive personalized feedback from your support team on assignments submitted

# 🙏 Contributions

We believe in the power of collaboration. Contributions, ideas, and feedback are highly encouraged! Let's build the ultimate resource for Agent Engineering at SRHG in 2026 together.

Please reach out to `chris@aimakerspace.io` with any questions or suggestions.
