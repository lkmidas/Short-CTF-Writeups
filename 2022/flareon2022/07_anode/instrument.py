code = open("./out/anode.js", "r").read().split("\n")

new_code = []

for line in code:
    if line.startswith("          b["):
        line = "          console.log(\"" + line[:-1].strip()
        if "Math.floor(Math.random() * 256)) & 0xFF" in line: 
            line = line.replace(" Math.floor(Math.random() * 256)) & 0xFF", "\", Math.floor(Math.random() * 256), \") & 0xFF\");")
        elif "Math.floor(Math.random() * 256)" in line:
            line = line.replace(" Math.floor(Math.random() * 256)", "\", Math.floor(Math.random() * 256));")
        else:
            line += "\");"
        #print(line)
    
    new_code.append(line + "\n")

f = open("./out/anode_new.js", "w")
for line in new_code:
    f.write(line)
    