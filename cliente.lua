--[[
Desenvolvido por Micaele Vieira e Rodrigo Leite

--]]

local socket = require ("socket")

local client = socket.connect('10.0.0.11',12345)

for i=1,100 do
	
	client:send("Passa a String"..'\n')

	local line,err = client:receive()
end
