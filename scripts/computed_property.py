from functools import wraps

def computed_property(*attrs):
    def decorator(func):
        @property # decorator para que se comporte como uma propriedade
        @wraps(func) # decorator para que a docstring seja mostrada ao executar o help()
        def wrapper(self):
            # restringe atributos àqueles existentes
            existing_attrs = [attr for attr in attrs if hasattr(self, attr)] 
            # cria o nome do cache como a junção do nome dos atributos
            cache_name = f"_{'_'.join(existing_attrs)}" 
            # cria a chave do cache como valor dos atributos
            cache_key = "_".join([str(getattr(self, attr)) for attr in existing_attrs])
            # se o cache ainda não está setado, seta-o como um dicionário 
            # com valores das variáveis como chave e a resposta da função como valor
            if not hasattr(self, cache_name):
                value = func(self)
                setattr(self, cache_name, {cache_key: value})
                return value
            # se já está setado, busca a cache_key nas chaves do cache.
            # caso esteja lá, apenas retorna seu valor; caso não, executa
            # a função, retorna seu resultado e o armazena no cache
            else:
                if cache_key not in getattr(self, cache_name).keys():
                    value = func(self)
                    getattr(self, cache_name).update({cache_key: value})
                    return value
                else:
                    return getattr(self, cache_name).get(cache_key)
        return wrapper
    return decorator