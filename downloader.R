# Get current timestamp
current_time <- format(Sys.time(), "%Y-%m-%d_%H-%M-%S")

# Write "Hi" to a file named with the current timestamp
write("Hi", paste0(current_time, ".txt"))