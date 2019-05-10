use super::*;

fn hexdump(bytes: &[u8]) -> String {
    bytes.into_iter()
        .map(|b| format!("{:02x}", b))
        .collect::<String>()
}

#[test]
fn test_check_pow_valid() {
    let mut v = Vec::new();
    v.extend_from_slice("e2ZgIzlOpe".as_bytes());
    let valid = check_pow(&mut v, 26, 52644528);
    assert!(valid);
}

#[test]
fn test_check_pow_invalid() {
    let mut v = Vec::new();
    v.extend_from_slice("e2ZgIzlOpe".as_bytes());
    let valid = check_pow(&mut v, 26, 1);
    assert!(!valid);
}

#[test]
fn test_pow_hash() {
    let mut v = Vec::new();
    v.extend_from_slice("e2ZgIzlOpe".as_bytes());
    let hash = pow_hash(&mut v, 52644528);
    assert_eq!("a51496f8ce009bab48108eaaa085b749b39c8707ae622e8d446a5c9228000000", hexdump(&hash));
}

#[test]
fn test_thread_loop(){
    let mut v = Vec::new();
    v.extend_from_slice("e2ZgIzlOpe".as_bytes());
    let r = guess_loop(&mut v, 13, 0);
    assert_eq!(r,2496);
}

#[test]
fn test_crack_pow(){
    let v = "e2ZgIzlOpe".as_bytes();
    let r = crack_pow(v.as_ptr(), v.len(), 13, 0);
    assert_eq!(r,2496);
}