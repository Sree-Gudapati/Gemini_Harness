import agent_interaction


def main():
    # long term chat storage
    memory = []

    interaction = agent_interaction.ModelInteract(memory)
    interaction.interact_loop()


if __name__ == "__main__":
    main()
