function axing(buff)   return (buff:gsub('..', function (z)     return string.char(tonumber(z, 16)-1)   end)) end
begin = {'0','1', '2','3','4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'} last = {'x','u','h','s','p','v','g','q','r','y','z','n','m','i','w','k'} function decr( buff ) if buff == nil then return '0' end local temp = buff for i=1,#begin do temp = string.gsub(temp, last[i], begin[i]) end return temp end
function reveser( str ) if str == nil then return '0' end local txt = '' for i=#str,1,-1 do local c = string.char(string.byte(str,i)) txt = txt .. c end return txt end
function axiang(buff) local temp = string.gsub(buff, "5", "z") temp = string.gsub(temp, "f", "5") temp = string.gsub(temp, "z", "f") temp = string.gsub(buff, "6", "z") temp = string.gsub(temp, "d", "6") temp = string.gsub(temp, "z", "d") return temp end
function xingxiang(str) return reveser(axing(axiang(decr(reveser(str))))) end
