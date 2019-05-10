# Proof of Work Calculator

## Deps

To build:
 - `docker` or `rust`

To run:
 - `python`

## Building

With rust installed:
```bash
cargo build --release
```
With docker installed:
```bash
docker run -it --rm -v $PWD:/host -u $(id -u):$(id -g) -w /host rust cargo build --release
```

## Testing

With rust installed:
```bash
cargo test
./proofofwork.py
```

With docker isntalled:
```bash
docker run -it --rm -v $PWD:/host -u $(id -u):$(id -g) -w /host rust cargo test
./proofofwork.py
```

## API

### rust

```rust
pub extern fn crack_pow(
	//The c_char_p pointing to the prefix string
	prefix: *const u8, 
	//The length of that prefix string
	prefix_len: usize, 
	//The number of required zero result bits
	kbits:u8, 
	//The place to begin looking (parallel requirement)
	start:u64
) -> u64
```

### python3

```python
solve_pow(
	#the challenge string
	prefix:str, 
	#the n many zero bits
	k:int
	#returns the successful integer
)
```

## Example

```python
import proofofwork
print(proofofwork.solve_pow("AAAAAAAAAA",26))
```
