## Size of the Dataset
DATA_SIZE = 9
## Name of the file
FILE_NAME = "test.log"

file_data = scan(FILE_NAME,,DATA_SIZE)
linux_time = 0
ac0 = 0
ac1 = 0

for(i in 1 : DATA_SIZE){
	print(file_data[i])
	}

for(i in 1 : DATA_SIZE) {
      if(i %% 3 == 1){
      	linux_time[i/3 + 1] = file_data[i]
      }
      if(i %% 3 == 2){
      	ac0[i/3 + 1] = file_data[i]
      }
      if(i %% 3 == 0){
      	ac1[i/3] = file_data[i]
      }
}

print("done")

for(i in 1 : 3){
	print(linux_time[i])
}
print("printing ac0")
for(i in 1 : 3){
	print(ac0[i])
}
print("printing ac1")
for(i in 1 : 3){
	print(ac1[i])
}

## Plotting the graph
plot(linux_time, ac0)
