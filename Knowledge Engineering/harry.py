from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain), hagrid),
    And(hagrid, dumbledore),
    (And(hagrid, dumbledore)),
    dumbledore
)

print(model_check(knowledge, rain))
