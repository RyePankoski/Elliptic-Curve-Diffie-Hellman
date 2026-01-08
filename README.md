# Elliptic Curve Diffie-Hellman (ECDH) Key Exchange

A from scratch implementation of ECDH showing how two parties can establish a secure connection over the internet. This includes a man-in-the-middle eavesdropper to show what a malicious agent would see.

## Demo Output

![image02](https://github.com/user-attachments/assets/f077263b-87b5-4105-a69d-c1a0c6c422b7)

EXAMPLE 
```
[ALICE] and [BOB] agree to a curve, in this case there is only secp256k1.
[ALICE] and [BOB] both use a specified point G that comes with the curve.

[ALICE] and [BOB] then both calculate their k * G,  A and B respectively. k = private_key, k * G = public_key
[ALICE] Sends their A to BOB: (20, 61)
[BOB] Sends their B to ALICE: (42, 39)

[ALICE] computes their shared secret: b_secret × A
[BOB] computes their shared secret: a_secret × B

[ALICE] Shared secret: (8, 4)
[BOB] Shared secret: (8, 4)

Man-in-the-middle saw: [secp256k1, (20, 61), (42, 39)]
```
Alice and Bob both arrive at the same secret point "(8,4)". The eavesdropper saw everything that was transmitted, but without the secret internal parameters, cannot compute the secret point.

---

## How It Works

### The Math

**Curve:** y² = x³ + 7 (mod 97)  
**Base Point:** G = (68, 74)

**Core Operations:**
- **Point Addition:** We use modular arithmetic to find points.
- **Scalar Multiplication:** k × G = G + G + ... (k times)
- **One-Way Property:** Easy to compute k × G, hard to find k from result

### The Protocol

1. **Alice:** Picks secret `a`, computes public key `A = a × G`, sends A
2. **Bob:** Picks secret `b`, computes public key `B = b × G`, sends B
3. **Alice:** Computes shared secret `a × B`
4. **Bob:** Computes shared secret `b × A`
5. **Both get the same result:** `(ab) × G`

This is an example of the commutative property in action. It encodes the secret parameter, while keeping it nigh impossible for a malicious agent to infer or compute.

The eacesdropper would need:
- Secret `a` or `b` to compute shared secret
- This is a good example of the elliptic curve discrete logarithm problem (ECDLP), in that it is computationally infeasible to reverse this operation.
But the only thing the eavesdropper sees is:
- G, A, B (all public)

**Key Functions:**
```python
scalar_multiply(k, point)   # Compute k × point
add_points(p1, p2)          # Point addition
double_point(p)             # Point doubling
find_mod_inv(n, p)          # Modular inverse for division
```

## Running

```bash
python main.py
```
---

## Educational Features

**Implemented from scratch:**
-  Modular arithmetic (no crypto libraries)
-  Point addition formulas (tangent/chord method)
-  Scalar multiplication
-  Edge cases (point at infinity, y=0)
-  Full ECDH protocol
-  Man-in-the-middle simulation
-  Finite field arithmetic (mod 97)
-  Elliptic curve geometry
-  Discrete logarithm hardness
-  Public-key cryptography principles
---


---

## Why This Matters

This exact protocol (with 256-bit numbers) secures:
- HTTPS/TLS (web browsing)
- Signal/WhatsApp (messaging)
- Bitcoin/Ethereum (transactions)
- SSH (remote access)
- VPNs (network tunnels)


**The math is identical in real systems, just a lot bigger**

This implementation uses mod 97 (not 17) because larger primes have points with higher order, avoiding "point at infinity" edge cases. Real systems use gigantic primes.

---

## The Internet Class

All communication between ALICE and BOB is routed through a shared `Internet` class that logs everything, there is no high level class coordination between them. 

```python
class Internet:
    messages = []              # Message queue
    man_in_the_middle = []     # What Eve sees
```

This **proves** the security model: Alice and Bob have no secret channel. Everything is public, yet the shared secret remains private. This is the magic of ECDH.
