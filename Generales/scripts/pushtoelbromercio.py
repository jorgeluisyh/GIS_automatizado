import os
import shutil


ruta_output = "output"
dirgenerales = os.path.dirname(os.path.dirname(__file__))
scriptsdir = os.path.join(dirgenerales, 'scripts')
sourcesdir = os.path.join(dirgenerales, 'sources')

def creamos_output():
    """
    Necesitamos crear el output, ya que es necesario por el repositorio cpina/github-action-push-to-another-repository@main
    se requiere que se cree una carpeta y a partir de ella se envíen los archivos
    """
    os.mkdir("output")


def copytree(src, dst, symlinks= False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

def main():
    creamos_output()
    src_path = os.path.join(sourcesdir, 'elBromercio')
    dst_path = ruta_output
    # Copiamos los archivos del repositorio a la ruta output
    copytree(src_path, dst_path)


if __name__ == '__main__':
    print(scriptsdir)
    print(sourcesdir)
    main()