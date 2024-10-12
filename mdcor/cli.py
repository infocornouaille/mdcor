import argparse
from mdcor.watcher import watch_directory
from mdcor.converts import batch_convert_latex, batch_convert_pdf

def main():
    parser = argparse.ArgumentParser(description="Surveillance et conversion des fichiers Markdown")
    parser.add_argument("--path", default=".", help="Chemin du dossier à surveiller ou à traiter")
    parser.add_argument("--interval", type=int, default=10, help="Intervalle de surveillance en secondes")
    parser.add_argument("--output", default=".", help="Dossier de sortie pour les fichiers convertis")
    parser.add_argument("--pdf", action="store_true", help="Convertir également en PDF lors de la surveillance")
    parser.add_argument("--template", default="eisvogel", help="Template LaTeX à utiliser pour la conversion PDF")
    parser.add_argument("--latex-all", action="store_true", help="Convertir tous les fichiers Markdown en LaTeX")
    parser.add_argument("--pdf-all", action="store_true", help="Convertir tous les fichiers Markdown en PDF")
    parser.add_argument("--bw", action="store_true", help="Convertir les images en noir et blanc")
    parser.add_argument("--max-size", type=int, nargs=2, help="Taille maximale des images (largeur hauteur)")

    args = parser.parse_args()

    convert_bw = args.bw
    max_size = tuple(args.max_size) if args.max_size else None

    if args.latex_all:
        batch_convert_latex(args.path, args.output, convert_bw, max_size)
    elif args.pdf_all:
        batch_convert_pdf(args.path, args.output, args.template, convert_bw, max_size)
    else:
        print(f"Surveillance du dossier {args.path} toutes les {args.interval} secondes...")
        watch_directory(args.path, args.interval, args.output, args.pdf, args.template, convert_bw, max_size)

if __name__ == "__main__":
    main()