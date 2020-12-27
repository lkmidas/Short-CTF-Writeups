-------------
version = '2.34NBVF'

function getVersion( ... )
  return version
end

require('wbit')

require('auto_functions')
delay_read = 0
delta = 0x9E3779B9

---------------------------------------------------------------------
-- Conversion
---------------------------------------------------------------------


function convertStringToBytes(str)
  local bytes = {}
  local strLength = string.len(str)
  for i=1,strLength do
    table.insert(bytes, string.byte(str, i))
  end

  return bytes
end


function convertBytesToString(bytes)
  local str = ''
  if bytes ~= nil then  
  local bytesLength = table.getn(bytes)
    for i=1,bytesLength do
      str = str .. string.char(bytes[i])
    end
  end
  return str
end


function convertHexStringToBytes(str)
  local bytes = {}
  local strLength = string.len(str)
  for k=2,strLength,2 do
    local hexString = '0x' .. string.sub(str, (k - 1), k)
    table.insert(bytes, hex.to_dec(hexString))
  end

  return bytes
end


function convertBytesToHexString(bytes)
  local str = ''
  local bytesLength = table.getn(bytes)
  for i=1,bytesLength do
    local hexString = string.sub(hex.to_hex(bytes[i]), 3)
    if string.len(hexString) == 1 then
      hexString = '0' .. hexString
    end
    str = str .. hexString
  end

  return str
end


function convertBytesToUIntArray(bytes, includeLength)
  local bytesLength = table.getn(bytes)
  local result = {}

  if includeLength then
    local n = bit.brshift(bytesLength, 2) + 1
    if bit.band(bytesLength, 3) ~= 0 then
      n = n + 1
    end

    result[n] = bytesLength;
  end

  for i=0,(bytesLength - 1) do
    local resultIndex = bit.brshift(i, 2) + 1
    if result[resultIndex] == nil then
      result[resultIndex] = 0
    end

    local resultValue = bit.blshift(bit.band(0x000000ff, bytes[i+1]), bit.blshift(bit.band(i, 3), 3))
    result[resultIndex] = bit.bor(result[resultIndex], resultValue);
  end

  return result
end


function convertUIntArrayToBytes(data, includeLength)
  local dataLength = table.getn(data)
  local n = bit.blshift(dataLength, 2)
  local result = {}

  if includeLength then
    local m = data[dataLength]
    if m > n then
      return nil
    end

    n = m
  end

  for i=0,(n-1) do
    local value = bit.band(bit.brshift(data[bit.brshift(i, 2) + 1], (bit.blshift(bit.band(i, 3), 3))), 0xff)
    table.insert(result, value)
  end

  return result
end


function convertToUInt32(value)
  if value < 0 then
    local absValue = math.abs(value)
    local a = math.floor(absValue / 0xFFFFFFFF)
    local b = value + a * 0xFFFFFFFF
    local c = 0xFFFFFFFF + b + 1
    return c
  end

  return math.mod(value, 0xFFFFFFFF) - math.floor(value / 0xFFFFFFFF)
end

---------------------------------------------------------------------
-- Encryption/decryption common
---------------------------------------------------------------------


function mx(sum, y, z, p, e, k)
  local aa = bit.brshift(z, 5)
  local ab = convertToUInt32(bit.blshift(y, 2))
  local ac = bit.bxor(aa, ab)

  local ba = bit.brshift(y, 3)
  local bb = convertToUInt32(bit.blshift(z, 4))
  local bc = bit.bxor(ba, bb)
  local ca = bit.bxor(sum, y)

  local dia = bit.band(p, 3)
  local dib = bit.bxor(dia, e)
  local da = k[dib + 1]
  local db = bit.bxor(da, z)

  local ea = convertToUInt32(ca + db)
  local fa = convertToUInt32(ac + bc)
  local ga = bit.bxor(fa, ea)

  return ga
end

---------------------------------------------------------------------
-- Decryption
---------------------------------------------------------------------


function decryptIntArray(v, k)
  local n = table.getn(v)
  local z = v[n]
  local y = v[1]
  local e = 0
  local p = 0

  local q = 6 + math.floor(52 / n)
  local sum = convertToUInt32(q * delta)
  while sum ~= 0 do
    e = bit.band(bit.brshift(sum, 2), 3)
    for p=n,2,-1 do
      z = v[p - 1]
      v[p] = convertToUInt32(v[p] - mx(sum, y, z, (p-1), e, k))
      y = v[p]
    end

    z = v[n]
    v[1] = convertToUInt32(v[1] - mx(sum, y, z, p, e, k))
    y = v[1]

    local sumBefore = sum
    sum = convertToUInt32(sum - delta)
  end

  return v
end


function decrypt(data, key)
  local dataLength = string.len(data)
  local keyLength = string.len(key)

  if keyLength == 0 then
    return data
  end

  local keyBytes = convertStringToBytes(key)
  local encryptedBytes = convertHexStringToBytes(data)

  local dataIntArray = convertBytesToUIntArray(encryptedBytes, false)
  local keyIntArray = convertBytesToUIntArray(keyBytes, false)

  local decryptedIntArray = decryptIntArray(dataIntArray, keyIntArray)
  local decryptedBytes = convertUIntArrayToBytes(decryptedIntArray, true)
  local decryptedString = convertBytesToString(decryptedBytes)

  return decryptedString
end

---------------------------------------------------------------------
-- Encryption
---------------------------------------------------------------------


function encryptIntArray(v, k)

  n = table.getn(v)
  if n < 2 then
    return v
  end

  local z = v[n]
  local y = v[1]
  local sum = 0
  local e = 0
  local p = 0
  local initQ = 6 + math.floor(52 / n)

  for q=initQ,1,-1 do
    sum = convertToUInt32(sum + delta);
    e = bit.band(bit.brshift(sum, 2), 3);
    for p=1,(n-1) do
      y = v[p + 1];
      v[p] = convertToUInt32(v[p] + mx(sum, y, z, (p-1), e, k));
      z = v[p]
    end
    y = v[1];
    v[n] = convertToUInt32(v[n] + mx(sum, y, z, (n-1), e, k));
    z = v[n]
  end

  return v;

end


buzhidao = 'nguyenviethung!0792cn'
keygen = '0'
ERROR_QUIT = {}


function getMainName( str )
  str = wstrToUtf8(str)
  local name = str
  local x = string.find(str, '@')
  if x ~= nil then
    name = string.sub(str,0,x-1)
  end
  return utf8ToWstr(name)
end


function create_auto()
  local t = {}
  t.JianCha = function ()
    local login_id = nx_execute('form_stage_login\\form_login', 'get_login_id')
    local inputvar = t.getCodeActive()
    if inputvar == nil or login_id == nil then return false end
    local strTable = util_split_string(nx_string(inputvar), ',')
    local id,time,name
    if #strTable == 3 then
      id = strTable[1]
      time = tonumber(strTable[2])
      name = nx_function('ext_utf8_to_widestr', strTable[3])
    else
      return false
    end

    if name ~= t.getCodeName() then
      return false 
    end

    local cur_time = t.getCurTime()
    if string.upper(nx_string(login_id)) == string.upper(nx_string(id)) and cur_time < time then
      return true 
    else
      return false 
    end
  end

  t.getCodeName = function ()
    local game_client = nx_value('game_client')
    local client_player = game_client:GetPlayer()
    if not (nx_is_valid(client_player)) then
      return nx_widestr('0')
    end
    local playerName = client_player:QueryProp('Name')
    return getMainName(nx_widestr(playerName))
  end

  t.getCurTime = function ()
    local MessageDelay = nx_value('MessageDelay')
    if not (nx_is_valid(MessageDelay)) then
      return 0
    end
    return MessageDelay:GetServerSecond()
  end

  t.getCodeActive = function ()
    local login_id = nx_execute('form_stage_login\\form_login', 'get_login_id')
    local file = nx_resource_path() .. 'auto9yin\\user\\' .. login_id .. '.ini'
    local checkkey = nx_string(IniRead(file, 'Auto', 'key', '0'))
    if string.len(checkkey) > 5 then 
      local key = decrypt(checkkey, buzhidao)
      return key
    end
    return 0
  end







  local proxy = {}
  local mt = {       -- create metatable
    __index = t,
    __newindex = function (t,k,v)
      table.insert(ERROR_QUIT,1)
    end
  }
  setmetatable(proxy, mt)
  return proxy
end


function getAuto()
  if Auto9Yin == nil then 
    Auto9Yin = create_auto() 
    nx_pause(2)
  end
  return Auto9Yin
end


function isLogin( ... )
  local login = nx_value('form_stage_login\\form_login')
  if nx_is_valid(login) and login.Visible then
    return true
  end
  return false
end

