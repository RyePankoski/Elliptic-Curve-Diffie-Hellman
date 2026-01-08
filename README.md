# Elliptic Curve Diffie-Hellman (ECDH) Key Exchange

A from-scratch Python implementation of ECDH demonstrating how two parties establish a shared secret over an insecure channel. Includes a man-in-the-middle observer to show what an eavesdropper would see.

**For a detailed mathematical explanation of why this works, see the accompanying paper: [How.to.send.a.secret.message-1.pdf](https://github.com/user-attachments/files/24510702/How.to.send.a.secret.message-1.pdf)

---

## Demo Output

![image02](https://github.com/user-attachments/assets/f077263b-87b5-4105-a69d-c1a0c6c422b7)

```
[ALICE] and [BOB] agree on curve parameters and base point G
[ALICE] Generates secret a, computes public key A = a×G
[BOB] Generates secret b, computes public key B = b×G
[ALICE] Sends A to BOB: (20, 61)
[BOB] Sends B to ALICE: (42, 39)
[ALICE] Computes shared secret: a×B = (8, 4)
[BOB] Computes shared secret: b×A = (8, 4)

Man-in-the-middle saw: [curve params, (20, 61), (42, 39)]
Cannot compute (8, 4) without knowing a or b
```

Alice and Bob arrive at the same shared secret point `(8, 4)` without ever transmitting their private keys. The eavesdropper sees all public communications but cannot compute the shared secret, this is the **elliptic curve discrete logarithm problem** (ECDLP) at work.

---

## Implementation Details

**Curve:** y² = x³ + 7 (mod 97)  
**Base Point:** G = (68, 74)

This toy example uses mod 97 for readability. Real systems (secp256k1, P-256) use 256-bit primes with identical mathematics.

### Core Operations

**Point Addition** : Geometric chord-and-tangent method:
```python
add_points(P, Q)     # Find third intersection point, reflect
```

**Scalar Multiplication** : Repeated point addition:
```python
scalar_multiply(k, P)  # Compute P + P + ... + P (k times)
```

**Modular Arithmetic:**
```python
find_mod_inv(n, p)   # Extended Euclidean algorithm for division
```

**Edge Cases Handled:**
- Point at infinity (group identity)
- Point doubling (tangent case)
- Vertical lines (y-coordinate = 0)

---

## The Protocol

1. **Public Setup:** Alice and Bob agree on curve equation, prime p, and base point G
2. **Private Keys:** Alice picks secret `a`, Bob picks secret `b`
3. **Public Keys:** Alice computes `A = a×G`, Bob computes `B = b×G`
4. **Exchange:** Alice sends A → Bob, Bob sends B → Alice (both public)
5. **Shared Secret:** 
   - Alice computes `a×B = a×(b×G) = (ab)×G`
   - Bob computes `b×A = b×(a×G) = (ab)×G`
   - Both arrive at the same point

**Security:** An eavesdropper sees G, A, and B but cannot compute `(ab)×G` without solving the ECDLP, finding `a` from `A = a×G` or `b` from `B = b×G`.

---

## Running the Code

```bash
python main.py
```

No external dependencies. Pure Python implementation of all cryptographic primitives.

---

## Educational Features

This implementation demonstrates:

**No crypto libraries** : All math implemented from scratch  
**Finite field arithmetic** : Modular addition, multiplication, inversion  
**Elliptic curve geometry** : Point addition using chord/tangent formulas  
**Scalar multiplication** : Efficient double-and-add algorithm  
**Full ECDH protocol** : End-to-end key exchange  
**Man-in-the-middle simulation** : Proves the security model  

### The `Internet` Class

All communication is routed through a shared `Internet` object that logs every transmission:

```python
class Internet:
    messages = []              # Message queue
    man_in_the_middle = []     # Everything Eve sees
```

Alice and Bob have **no private channel** :everything goes through `Internet`. This proves the security model: even with complete visibility into all transmitted data, the shared secret remains private.

---

## Real-World Applications

This exact protocol (scaled to 256-bit numbers) secures:

- **HTTPS/TLS** : Web browsing
- **Signal/WhatsApp** : End-to-end encrypted messaging  
- **Bitcoin/Ethereum** : Transaction signing
- **SSH** : Secure remote access
- **VPNs** : Encrypted network tunnels

**The mathematics are identical, just scaled up.** This toy example uses a 7-bit prime (97); production systems use 256-bit primes (~10^77).

---

## Further Reading

For a complete mathematical explanation covering:
- Why finite fields resist inversion
- The discrete logarithm problem  
- Why prime moduli are required
- How elliptic curves defeat index calculus
- The geometric construction of point addition

---

## License

MIT
