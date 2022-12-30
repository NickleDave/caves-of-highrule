import highrule

parser = highrule.parser.get_parser()
args = parser.parse_args()
highrule.main.main(debug=args.debug)
