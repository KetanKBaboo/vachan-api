'''Utility functions to be used in graphql API implementations'''

def convert_graphene_obj_to_pydantic(input_obj, target_class):
    '''convert a graphene input object into specified pydantic model'''
    kwargs = {}
    for key in input_obj:
        kwargs[key] = input_obj[key]
    new_obj = target_class(**kwargs)
    return new_obj
