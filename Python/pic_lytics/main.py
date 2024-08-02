# python main.py treinar --dados dados/treinamento
# python main.py classificar --modelo modelo_treinado.h5 --imagens dados/teste
# pip install -r requirements.txt

import argparse
from treinamento import treinar_modelo
from classificar import classificar_imagens

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Treinar e classificar imagens.')
    subparsers = parser.add_subparsers(dest='comando', help='Comando a ser executado')

    # Comando 'treinar'
    parser_treinar = subparsers.add_parser('treinar', help='Treinar o modelo')
    parser_treinar.add_argument('--dados', required=True, help='Caminho para a pasta de dados de treinamento')

    # Comando 'classificar'
    parser_classificar = subparsers.add_parser('classificar', help='Classificar imagens')
    parser_classificar.add_argument('--modelo', required=True, help='Caminho para o modelo treinado')
    parser_classificar.add_argument('--imagens', required=True, help='Caminho para a pasta de imagens de teste')

    args = parser.parse_args()

    if args.comando == 'treinar':
        treinar_modelo(args.dados)
    elif args.comando == 'classificar':
        classificar_imagens(args.modelo, args.imagens)
    else:
        parser.print_help()