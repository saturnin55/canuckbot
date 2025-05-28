# Canucks Soccer Chat Discord Bot based on <a href="https://github.com/kkrypt0nn/Python-Discord-Bot-Template">Python Discord Bot Template</a>

<p align="center">
  <a href="https://discord.gg/mTBrXyWxAF"><img src="https://img.shields.io/discord/739934735387721768?logo=discord"></a>
  <a href="https://github.com/saturnin55/canuckbot/releases"><img src="https://img.shields.io/github/v/release/saturnin55/canuckbot"></a>
  <a href="https://github.com/saturnin55/canuckbot/commits/main"><img src="https://img.shields.io/github/last-commit/saturnin55/canuckbot"></a>
  <a href="https://github.com/saturnin55/canuckbot/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/saturnin55/canuckbot"></a>
  <a href="https://github.com/saturnin55/canuckbot"><img src="https://img.shields.io/github/languages/code-size/saturnin55/canuckbot"></a>
  <a href="https://conventionalcommits.org/en/v1.0.0/"><img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

This repository is a template that everyone can use for the start of their Discord bot.

When I first started creating my Discord bot it took me a while to get everything setup and working with cogs and more.
I would've been happy if there were any template existing. However, there wasn't any existing template. That's why I
decided to create my own template to let **you** guys create your Discord bot easily.

Please note that this template is not supposed to be the best template, but a good template to start learning how
discord.py works and to make your own bot easily.

If you plan to use this template to make your own template or bot, you **have to**:

- Keep the credits, and a link to this repository in all the files that contains my code
- Keep the same license for unchanged code

See [the license file](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/master/LICENSE.md) for more
information, I reserve the right to take down any repository that does not meet these requirements.

## Support

Before requesting support, you should know that this template requires you to have at least a **basic knowledge** of
Python and the library is made for **advanced users**. Do not use this template if you don't know the
basics or some advanced topics such as OOP or async. [Here's](https://pythondiscord.com/pages/resources) a link for resources to learn python.

If you need some help for something, do not hesitate to join my Discord server [here](https://discord.gg/mTBrXyWxAF).

All the updates of the template are available [here](UPDATES.md).

## Disclaimer

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here
```

When using the template you confirm that you have read the [license](LICENSE.md) and comprehend that I can take down
your repository if you do not meet these requirements.

## How to download it

This repository is now a template, on the top left you can simply click on "**Use this template**" to create a GitHub
repository based on this template.

Alternatively you can do the following:

- Clone/Download the repository
  - To clone it and get the updates you can definitely use the command
    `git clone`
- Create a Discord bot [here](https://discord.com/developers/applications)
- Get your bot token
- Invite your bot on servers using the following invite:
  https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS (
  Replace `YOUR_APPLICATION_ID_HERE` with the application ID and replace `PERMISSIONS` with the required permissions
  your bot needs that it can be get at the bottom of a this
  page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## How to set up

To set up the bot it was made as simple as possible.

### `config.json` file

There is [`config.json`](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

| Variable                  | What it is                                     |
| ------------------------- | ---------------------------------------------- |
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands |

### `.env` file

To set up the bot you will have to make use of the [`.env.example`](.env.example) file, you should rename it to `.env` and provide your bot's `TOKEN`, `INVITE_LINK`, and the location of your database in `DB_PATH`.

Alternatively, simply create the appropriate environmental variables in your operating system.

## CanuckBot specific 

- you will need to create a dedicated test discord server
- invite the bot
- create the database (see the setup folder, import the dump file into a new database)
- run the bot
- use config commands to set channel_logs, channel_cmds, default_category, mngr_roleid
- in the cogs/ folder, create a new file and add your set of commands
- in the CanuckBot/ folder, add your classes

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note** You may need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.

## Linting and Formatting

Ruff is used as the linter and formatter. It is installed as part of the requirements, and is run using a pre-commit hook defined in the .githooks folder. Ruff can also be installed as an extension for your code editor for inline hints.

Use `git config core.hooksPath .githooks` to set the hooks directory for this repository.

## Issues or Questions

If you have any issues or questions of how to code a specific command, you can:

- Join my Discord server [here](https://discord.gg/mTBrXyWxAF)
- Post them [here](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/issues)

Me or other people will take their time to answer and help you.

## Versioning

We use [SemVer](http://semver.org) for versioning. For the versions available, see
the [tags on this repository](https://github.com/kkrypt0nn/Python-Discord-Bot-Template/tags).

## Built With

- [Python 3.11.5](https://www.python.org/)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details
