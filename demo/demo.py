from dgad.prediction import Detective
from dgad.prediction import pretty_print

mydomains = ["adslkfjhsakldjfhasdlkf.com"]
detective = Detective()
# convert mydomains strings into dgad.schema.Domain
mydomains, _ = detective.prepare_domains(mydomains)
# classify them
detective.investigate(mydomains)
# view result, drops padded_token_vector for pretty printing
pretty_print(mydomains, output_format="json")
