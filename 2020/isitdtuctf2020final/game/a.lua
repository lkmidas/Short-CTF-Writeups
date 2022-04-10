package.path = package.path .. ";/path/to/bit.lua"
require 'bit.lua'
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


function decrypt()
  local keyBytes = convertStringToBytes('nguyenviethung!0792cn')
  local encryptedBytes = {194, 186, 198, 40, 236, 39, 94, 95, 157, 100, 164, 3, 165, 122, 244, 233, 136, 11, 164, 106, 231, 133, 96, 204, 11, 38, 246, 214, 48, 201, 58, 91, 195, 21, 48, 152, 247, 126, 122, 135, 31, 231, 199, 72, 79, 114, 243, 107, 196, 43, 250, 158, 14, 51, 28, 24, 110, 51, 100, 107, 220, 97, 201, 242, 25, 88, 203, 229, 220, 100, 104, 235, 132, 103, 111, 153, 194, 80, 75, 167, 184, 186, 41, 70, 62, 156, 72, 28, 17, 130, 196, 167, 24, 210, 228, 94, 178, 172, 234, 102, 77, 16, 36, 158, 143, 52, 221, 168, 1, 229, 105, 46, 203, 62, 78, 52, 55, 85, 137, 211, 140, 206, 64, 24, 160, 4, 199, 236, 156, 104, 5, 194, 122, 45, 55, 196, 82, 144, 195, 143, 125, 124, 230, 121, 118, 37, 103, 219, 47, 221, 68, 48, 159, 116, 54, 92, 24, 49, 6, 115, 246, 185, 141, 153, 161, 162, 126, 34, 4, 85, 91, 61, 18, 17, 60, 196, 199, 43, 102, 85, 72, 195, 115, 139, 226, 227, 16, 32, 106, 104, 232, 154, 30, 91, 228, 146, 172, 0, 171, 194, 42, 202, 80, 153, 253, 247, 225, 66, 109, 130, 175, 137, 175, 83, 216, 168, 66, 85, 0, 45, 22, 99, 82, 137, 13, 162, 254, 136, 129, 69, 13, 131, 111, 201, 90, 226, 140, 159, 96, 74, 203, 0, 211, 207, 149, 203, 42, 175, 20, 69, 240, 209, 35, 77, 225, 186, 209, 55, 57, 230, 209, 139, 61, 7, 24, 171, 209, 12, 37, 150, 53, 182}

  local dataIntArray = convertBytesToUIntArray(encryptedBytes, false)
  local keyIntArray = convertBytesToUIntArray(keyBytes, false)

  local decryptedIntArray = decryptIntArray(dataIntArray, keyIntArray)
  local decryptedBytes = convertUIntArrayToBytes(decryptedIntArray, true)
  local decryptedString = convertBytesToString(decryptedBytes)

  return decryptedString
end

print(decrypt())
