# Function to write a single register
def write_register(bus, address, register, value):
  bus.write_byte_data(address, register, value)

# Function to read a single register
def read_register(bus, address, register):
  return bus.read_byte_data(address, register)

def read_signed_16(bus, dev_add, high_reg, low_reg):
  return (lambda val : val if val < 32768 else val - 65536)((read_register(bus, dev_add, high_reg) << 8) | read_register(bus, dev_add, low_reg))

# Function to select the user bank
def select_user_bank(bus, address, bank_sel, bank):
  write_register(bus, address, bank_sel, bank)