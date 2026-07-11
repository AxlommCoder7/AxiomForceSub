import asyncio
import os
import signal
from config import GIT_BRANCH


# =====================================================
# Run Command
# =====================================================

async def run(command: str):

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return (
        process.returncode,
        stdout.decode().strip(),
        stderr.decode().strip()
    )


# =====================================================
# Git Status
# =====================================================

async def git_status():

    return await run(
        "git status"
    )


# =====================================================
# Git Pull
# =====================================================

async def git_pull():

    return await run(
        f"git pull origin {GIT_BRANCH}"
    )


# =====================================================
# Git Fetch
# =====================================================

async def git_fetch():

    return await run(
        "git fetch --all"
    )


# =====================================================
# Git Reset
# =====================================================

async def git_reset():

    return await run(
        f"git reset --hard origin/{GIT_BRANCH}"
    )


# =====================================================
# Git Branch
# =====================================================

async def current_branch():

    return await run(
        "git branch --show-current"
    )


# =====================================================
# Git Log
# =====================================================

async def git_log(limit=10):

    return await run(
        f"git log --oneline -{limit}"
    )


# =====================================================
# Latest Commit
# =====================================================

async def latest_commit():

    return await run(
        "git log -1 --pretty=format:'%H%n%an%n%ad%n%s'"
    )


# =====================================================
# Git Diff
# =====================================================

async def git_diff():

    return await run(
        "git diff"
    )


# =====================================================
# Git Remote
# =====================================================

async def git_remote():

    return await run(
        "git remote -v"
    )


# =====================================================
# Git Stash
# =====================================================

async def git_stash():

    return await run(
        "git stash"
    )


# =====================================================
# Git Restore
# =====================================================

async def git_restore():

    return await run(
        "git restore ."
    )


# =====================================================
# Git Clean
# =====================================================

async def git_clean():

    return await run(
        "git clean -fd"
    )


# =====================================================
# Restart
# =====================================================

def restart():

    os.kill(
        os.getpid(),
        signal.SIGINT
    )
