from io import DEFAULT_BUFFER_SIZE

def last_lines(file_path: str, bytes_chunk_size: int = DEFAULT_BUFFER_SIZE):
    # lê o arquivo
    with open(file_path,"r") as file:
        data=file.read()
    # inverte a ordem das linhas no arquivo
    data = "\n".join(reversed(data.split("\n"))) + "\n"
    # define a contagem de bytes e a linha que será o output da função
    bytes_count, line = 0, ""
    # itera sobre cada caractere do conteúdo do arquivo e agrega 
    # seu tamanho no bytes_count e seu valor na linha de output
    for i, chr in enumerate(data):
        bytes_count += len(chr.encode("utf-8"))
        line += chr
        # se há uma quebra de linha, se é o fim do arquivo ou se a contagem de
        # bytes atingiu o tamanho de chunk especificado, então a linha é retornada
        # e a contagem de bytes e a linha são "limpos"
        if (
            chr == "\n" or 
            i == len(data)-1 or
            bytes_count == bytes_chunk_size
        ):
            yield line
            bytes_count, line = 0, ""