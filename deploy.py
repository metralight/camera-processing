import os, shutil
import logging
import subprocess
import hjson

excludes = []
def deploy():
    # logging.info("Delete exe") 
    # if os.path.exists("cameraProcessing.exe"):
    #     os.remove("cameraProcessing.exe")

    # buildnout
    logging.info("Building main exe") 
    buildOutput = subprocess.check_output("py -3.8 -m PyInstaller --clean --log-level DEBUG  --distpath ./ server.spec", stderr=subprocess.STDOUT, shell=True, encoding="utf-8")
    if "Building EXE from EXE-00.toc completed successfully" not in buildOutput:
        logging.error("Pyinstall failed !")
        return

    # logging.info("Building plot exe") 
    # buildOutput = subprocess.check_output("py -3.9 -m PyInstaller --clean --onefile --log-level DEBUG  --distpath ./ plotProfilesApp.spec", stderr=subprocess.STDOUT, shell=True, encoding="utf-8")
    # if "Building EXE from EXE-00.toc completed successfully" not in buildOutput:
    #     logging.error("Pyinstall failed !")
    #     return

    logging.info("Clear deploy directory") 

    DEPLOY_DIR = 'deploy'

    # vycistit deploy adresar
    for file in os.listdir(DEPLOY_DIR):
        if file in excludes:
            continue

        path = os.path.join(DEPLOY_DIR, file)
        if (os.path.isdir(path)):
            shutil.rmtree(path)
        else:
            os.remove(path)

    # zkopirovat exe a nutne soucasti 
    logging.info("Fill deploy directory") 
    os.mkdir(os.path.join(DEPLOY_DIR, "logs"))
    os.mkdir(os.path.join(DEPLOY_DIR, "debug"))
    shutil.copytree("./www/public", os.path.join(DEPLOY_DIR, "www/public"))
    shutil.copy("cameraProcessing.exe", DEPLOY_DIR)
    shutil.copy("config.hjson", DEPLOY_DIR)
    shutil.copy("cameraConfig.hjson", DEPLOY_DIR)

    # empty userSettings
    hjson.dump({"CAMERA" : {}}, open(os.path.join(DEPLOY_DIR, "userSettings.hjson"), "w"))

    # smazat vygenerovany exe z rootu
    os.remove("cameraProcessing.exe")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    deploy()

