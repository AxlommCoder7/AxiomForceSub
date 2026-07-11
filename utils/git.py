#AxiomForceSub --by OwnerAxiom
import subprocess


def git_pull():

    try:

        out = subprocess.check_output(
            "git pull",
            shell=True,
            stderr=subprocess.STDOUT
        ).decode()

        return True, out

    except Exception as e:

        return False, str(e)
