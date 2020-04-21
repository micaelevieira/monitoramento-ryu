--[[
Desenvolvido por Micaele Vieira e Rodrigo Leite
--]]

--importanto socket
local socket = require ("socket")

--Criando String de 1K
kstring = {}
for i=1,999 do
	kstring[#kstring+1] = tostring(i%10)
end

kstring[#kstring+1] = "\n"
kstring = table.concat(kstring)

-- Criando socket TCP e ligando ao local host.

local server=assert(socket.bind("*",12345))

-- Descobrir qual porta o sistema operacional escolheu para nós
local ip,porta = server:getsockname()

print("Por favor, conecte na porta ", porta)

-- Aceitando uma conexão
local client,status = server:accept()

-- Marca o inicio da contagem do tempo
starttime = socket.gettime()
local cont = 0
while 1 do

	-- Não bloquear a linha de espera do cliente
	client:settimeout(2)
	-- Recebendo dados
	local line,err = client:receive()
	-- Se não ocorrer erro, envia de volta ao cliente
	if not err then 
		client:send(kstring.."\n")
	elseif err then
		break
	end
	
end

--Fechando a conexão com o cliente
client:close()
-- Marca fim da contagem do Tempo
endtime = socket.gettime()

--Tempo de duração
timediff = endtime-starttime
print("Fim do loop\n\t durou: "..string.format("%.4f", timediff).."s")
