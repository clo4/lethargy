"""
## What needs to be tested?

* Named
  - [ ] prettynames sorts by length alphabetically
  - [ ] index finds correct index
  - [ ] index raises indexerror if not found
  - [ ] index raises exc instead of indexerror if set

* Requirable
  - [ ] check_required returns missingoption if required
  - [ ] check_required returns none if not required

* Transforms
  - [ ] metavar gets name of type if tfm is a type
  - [ ] metavar gets default if tfm is not a type
  - [ ] transform calls tfm on value
  - [ ] transform exception raises a transformerror of the original

"""
