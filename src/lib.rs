#![allow(unused_variables)]
#![allow(dead_code)]

extern crate sha2;
extern crate byteorder;

use sha2::{Sha256, Digest};
use byteorder::{LittleEndian, WriteBytesExt, BigEndian, ReadBytesExt};

#[inline]
fn pow_hash(challenge: &mut Vec<u8>, solution: u64) -> Vec<u8> {
    //copy in the proposed solution
    challenge.write_u64::<LittleEndian>(solution).unwrap();
    //calculate the sha256
    let r = Vec::from(Sha256::digest(&challenge).as_slice());
    //remove the u64 solution
    challenge.truncate(challenge.len()-8);
    r
}

#[inline]
fn check_pow(challenge: &mut Vec<u8>, k: u8, solution: u64) -> bool {
	//calc sha256
    let h = pow_hash(challenge, solution);
    //take last 8 bytes
    let num = (&h[24..]).read_u64::<BigEndian>().unwrap();
    //mask off k bits
    let op = (1u64<<k)-1;
    //check if the final bits are 0s
    (num & op) == 0
}

#[inline]
fn guess_loop(challenge: &mut Vec<u8>, k:u8, start: u64) -> u64 {
	//separate for testing purposes
	let mut guess = start;
	while !check_pow(challenge, k, guess){
		guess += 1;
	}
	guess
}

#[no_mangle]
pub extern fn crack_pow(prefix: *const u8, prefix_len: usize, kbits:u8, start:u64) -> u64 {
	//copy the c input array
	let ffi_prefix = unsafe {
		Vec::from_raw_parts(prefix as *mut u8,prefix_len,prefix_len)
	};
	let mut prefix = ffi_prefix.clone();
	//let the caller do the free on the input data
	std::mem::forget(ffi_prefix);
	//??? -> profit
	guess_loop(&mut prefix, kbits, start)
}

#[cfg(test)]
mod test;