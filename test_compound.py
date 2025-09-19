#!/usr/bin/env python
"""Test script demonstrating Groq Compound model capabilities."""

import os
from groq_cli.chat import ChatCompleter
from rich.console import Console

console = Console()


def test_compound_features():
    """Test various compound model capabilities."""

    console.print("[bold cyan]Groq Compound Model Demo[/bold cyan]")
    console.print("=" * 50)

    chat = ChatCompleter()

    # Test 1: Web Search
    console.print("\n[yellow]1. Testing Web Search Capability:[/yellow]")
    query1 = "What's the current temperature in Tokyo right now?"
    console.print(f"Query: {query1}\n")
    result1 = chat.stream_completion(
        query=query1,
        model="groq/compound",
        temperature=0.5,
        maintain_history=False
    )
    if result1.get("tools_used"):
        console.print(f"\n[green]Tools used: {', '.join(result1['tools_used'])}[/green]")

    # Test 2: Code Execution
    console.print("\n\n[yellow]2. Testing Code Execution:[/yellow]")
    query2 = "Calculate the factorial of 12 using Python"
    console.print(f"Query: {query2}\n")
    result2 = chat.stream_completion(
        query=query2,
        model="groq/compound-mini",  # Use mini for single tool
        temperature=0.2,
        maintain_history=False
    )
    if result2.get("tools_used"):
        console.print(f"\n[green]Tools used: {', '.join(result2['tools_used'])}[/green]")

    # Test 3: Research with Domain Filtering
    console.print("\n\n[yellow]3. Testing Research with Domain Filtering:[/yellow]")
    query3 = "Find recent scientific papers about quantum computing"
    console.print(f"Query: {query3}")
    console.print("[dim]Limiting to: arxiv.org, nature.com[/dim]\n")
    result3 = chat.stream_completion(
        query=query3,
        model="groq/compound",
        temperature=0.6,
        maintain_history=False,
        include_domains=["arxiv.org", "nature.com", "science.org"]
    )
    if result3.get("tools_used"):
        console.print(f"\n[green]Tools used: {', '.join(result3['tools_used'])}[/green]")

    console.print("\n" + "=" * 50)
    console.print("[bold green]Compound model tests completed![/bold green]")
    console.print("\n[dim]Note: The compound model automatically selects appropriate tools[/dim]")
    console.print("[dim]based on the query without any additional configuration.[/dim]")


if __name__ == "__main__":
    test_compound_features()