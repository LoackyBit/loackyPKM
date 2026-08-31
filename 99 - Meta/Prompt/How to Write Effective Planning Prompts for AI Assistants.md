---
status: permanent
type: concept
area: tech
related: []
source: original
title: "How to Write Effective Planning Prompts for AI Assistants"
date: '2026-01-22'
updated: 2026-01-22T10:51
tags: [tech/tech, tech/prompting, tech/ai, tech/planning]
summary: "The traditional way of writing instructions for intelligent AI assistants involves a highly specific approach: providing every detail, every coordinate, every variable, and expecting the model to e..."
---
[[Home MOC|Home]] / [[Tech & AI]] / [[How to Write Effective Planning Prompts for AI Assistants]]

# How to Write Effective Planning Prompts for AI Assistants

## Introduction to a Different Approach

The traditional way of writing instructions for intelligent AI assistants involves a **highly specific approach**: providing every detail, every coordinate, every variable, and expecting the model to execute the task perfectly on the first attempt. However, there exists a more effective alternative, particularly when tackling **complex projects where initial uncertainty is significant**.

This alternative method consists of starting with a vague description of the problem, then entering into an **iterative and collaborative dialogue** with the AI model. The goal is not to obtain working code on the first request, but rather to co-develop a **structured plan** that progressively clarifies project details and identifies critical points.

## The Limitation of the Ultra-Specific Approach

Many developers instinctively follow the path of maximum precision: they describe the problem in minute detail, specify every variable, every map coordinate, every system parameter. This works perfectly when you have **high confidence** in the expected outcome and a clear understanding of how to solve the problem.

However, this approach has a critical limitation: when facing **significant uncertainties** or more complex projects, the amount of initial detail does not guarantee success at all. In fact, it often leads to a frustrating cycle of corrections, refinements, and adjustments that consume time and computational resources (and therefore money) inefficiently.

## The Vague and Iterative Method

A radically different approach consists of **starting vague**. Rather than listing every detail, you describe the problem in general terms:

> "I'm trying to draw a border around the map and it's not working. Help me create a plan to solve this."

This approach leverages a fundamental capability of modern AI models: the ability to **identify and clarify gaps in the context you provide**. When you present a vague yet genuine description of your problem, the model does not proceed directly to generate code; instead, it enters **collaborative planning mode**.

## How Planning Mode Works

When you use a "planning mode" (available in advanced AI assistants like Claude Opus), the model does not generate code immediately. Instead:

1. **Analyzes the problem** in its initial form
    
2. **Formulates clarifying questions** to better understand your objectives
    
3. **Identifies critical points** that require architectural decisions
    
4. **Proposes a general outline** of how to approach the problem
    

Throughout this iterative dialogue, your input and answers allow the model to **progressively refine the plan** until it reaches the level of detail necessary to proceed with implementation.

## The Difference Between Vague and Imprecise

It's important to distinguish between vague and imprecise. **Vague means broad**, but still anchored to a concrete reality of your project. When you say "I have a player entity that moves on a map defined by coordinates between 0 and 500, and I want it to not be able to exit the visible borders," you're providing concrete information without entering implementation details.

By contrast, **imprecise means ambiguous or confused**, which doesn't help anyone.

## The Strategy for Large Projects

For **building large systems** where the architecture is not completely clear from the start, the iterative approach offers significant advantages:

- **Reduces risk** of making wrong architectural decisions in implementation details
    
- **Progressively clarifies** the problem domain
    
- **Maintains flexibility** to adapt to discoveries during the planning process
    
- **Consumes fewer computational resources** compared to iterative code-test-correct cycles
    

## Choosing the Right AI Model

In today's AI model landscape, not all models are equivalent for the planning task:

## Opus 4.5 vs GPT-5.2 Code (Codeex)

**Opus 4.5** (by Anthropic) is a model that tends to **generate more detailed and discursive output**. It provides extensive explanations, rich context, and arguments its choices. This verbosity comes at a cost: it consumes more output tokens, which translates to **higher computational costs**.

**GPT-5.2 Code** (Codeex by OpenAI) adopts a **concise and direct approach**. It produces quick solutions, gets straight to the point, and provides only the bare essentials. It's like communicating with a **taciturn senior engineer**: it gets the job done, but with few additional explanations.

**Open Source Models** like Alibaba's GLM represent an **economically advantageous alternative**, offering comparable performance for specific tasks at a fraction of the cost.

## Which One to Choose?

For **planning and problem-solving**, Opus tends to be more useful despite the higher cost: its verbosity allows you to obtain clarifications, alternative reasonings, and considerations of aspects you may not have anticipated. For **direct implementation and point corrections**, Codeex or more efficient open-source models may be adequate.

## Extreme Alternatives: Spec-Driven Development

There is a further evolution of this approach, practiced by some teams specialized in **AI-powered development**. It consists of **writing the entire specification in markdown**, creating a planning document so detailed that the model can subsequently implement the code almost mechanically.

The process works like this:

1. **Planning phase**: You dialogue with the model (often in extended reasoning mode) to develop a complete specification
    
2. **Save to markdown**: The plan is exported to a structured file
    
3. **Review and verification**: The specification is reexamined for logical consistency and feasibility
    
4. **Implementation**: Only then does the model generate code based on the plan
    
5. **Iterate on the plan**: If the code contains errors, you return to the plan, correct it, and regenerate the code
    

This method has gained several names in technical jargon: **spec-driven development**, **markdown-first development**, and others. The real value lies in the recognition that a **quality plan is the foundation** of quality implementation.

## The Role of Structuring in Prompts

A frequently discussed topic in the developer community concerns the **best format for structuring information** within prompts: XML, markdown, or something else?

## XML and Markdown in Modern Models

Historically, **XML was the privileged format** in modern LLMs because a significant portion of training included examples structured in XML. This allowed models to clearly distinguish between different sections of text, avoiding confusion when pasting code or documentation with special characters.

In **current-generation models**, however, this necessity has diminished. Models are sufficiently sophisticated to analyze **properly formatted markdown** without losing sense of structure. The ability to discern the difference between an instruction section, a code block, and another documentation section is now robust.

## When to Still Use XML

Although no longer mandatory, **XML retains practical value** in certain scenarios:

- When pasting **very long documentation** with code examples interspersed
    
- When **extreme disambiguation** is required between contents of different types
    
- When working with complex documents that might contain multiple code blocks with backticks
    

## For System Instruction Files

For "agent instruction" files — that is, system instructions attached to **every single conversation** to maintain model coherence and behavior — using **markdown is completely adequate**. You're not writing a book; you're providing a list of rules and contexts the model should remember. Markdown is readable, organized, and sufficient.

## Conclusion: A Paradigm Shift

The paradigm shift consists of recognizing that **iterative planning is more efficient than ultra-precise specifications for complex projects**. It's not a limitation of AI models, but rather a recognition that **collaborative reasoning produces better results** than unidirectional commands.

Starting vague, dialoguing, clarifying, refining, and finally implementing: this is the cycle that **reduces total time**, **limits computational resource waste**, and produces more solid architectures because they've been thought through critically rather than generated hastily.

---
## Collegamenti
- [[Mastering AI Prompting]]
