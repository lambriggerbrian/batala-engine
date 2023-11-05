from numpy import uint32, left_shift, int8, uint64

INDEX_BITS = 24
GENERATION_BITS = 8
INDEX_MASK = left_shift(uint32(1), INDEX_BITS) - 1
GENERATION_MASK = left_shift(uint32(1), GENERATION_BITS) - 1
MAX_ENTITIES = 2**INDEX_BITS
MAX_GENERATIONS = 2**GENERATION_BITS
MINIMUM_FREE_INDICES = 1024

Id = uint32
Index = uint32
Generation = int8

ModuleId = int
