// resource: https://en.wikipedia.org/wiki/RC4
use std::char;
use std::fs;
use std::env;

// key scheduler
fn ksa(key: &str) -> [i32; 256] {
    let keylength: usize = key.len();
    let mut s: [i32; 256] = [0; 256];
    for i in 0..256 {
        s[i] = i as i32;
    }
    let mut j: i32 = 0;
    for i in 0..256 {
        let kcode = key.chars().nth(i % keylength).unwrap() as i32;
        j = (j + s[i] + kcode) % 256;
        swap(&mut s, i, j as usize);
    }
    return s;
}

// generation
fn prga(mut s: [i32; 256], plain: &str) -> Vec<i32> {
    let mut i: usize = 0;
    let mut j: usize = 0;
    let mut stream: Vec<i32> = Vec::new();
    for _x in 0..plain.len() {
        i = (i + 1) % 256;
        j = (j + s[i] as usize) % 256;
        swap(&mut s, i, j);
        let k: i32 = s[((s[i] + s[j]) % 256) as usize];
        stream.push(k);
    }
    return stream;
}

fn swap(a_data: &mut [i32; 256], i0: usize, i1: usize) {
    a_data[i0] = a_data[i0] ^ a_data[i1];
    a_data[i1] = a_data[i1] ^ a_data[i0];
    a_data[i0] = a_data[i0] ^ a_data[i1];
}

fn encrypt(plain: &str, stream: Vec<i32>) -> Vec<i32> {
    let mut encrypted = Vec::new();
    for i in 0..plain.len() {
        let nc = plain.chars().nth(i).unwrap() as i32;
        encrypted.push(stream[i] ^ nc);
    }
    return encrypted;
}

fn decrypt(encrypted: Vec<i32>, stream: Vec<i32>) -> String {
    let mut plain: String = String::new();
    for i in 0..encrypted.len() {
        let next_char = char::from_u32((stream[i] ^ encrypted[i]) as u32);
        plain += &next_char.unwrap().to_string();
    }
    return plain;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if "--help" == &args[1] || "-h" == &args[1] || args.len() < 3 {
        println!("\nRC4, Rust Implementation\nFirst arg: file directory you want to encrypt\nSecond arg: key to encrypt with\n");
        return;
    }
    let dir = &args[1];
    let input = &fs::read_to_string(dir).expect("PANIC! File couldn't be loaded.");
    let key = &args[2];
    let stream = prga(ksa(key), input);
    println!("\nStream:\n{:?}\n", stream);
    let encrypted_data = encrypt(input, stream.clone());
    let plain = decrypt(encrypted_data, stream.clone());
    assert_eq!(input.to_string(), plain);
    print!("Plain text:\n{}\n", plain);
}
