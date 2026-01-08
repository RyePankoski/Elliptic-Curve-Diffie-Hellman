# Elliptic Curve Diffie-Hellman (ECDH) Key Exchange

A from scratch implementation of ECDH showing how two parties can establish a secure connection over the internet. This includes a man-in-the-middle eavesdropper to show what a malicious agent would see.

If you would like to see a very detailed write up what exactly is going on, and why this works so well in cryptograhy, see the bottom of the readme.

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


# Why Elliptic Curves: Understanding the Discrete Logarithm Problem

#THE FIELD

The set R (real numbers) is monotonic (functionally, it always grows. n + 1 > n) This creates isomorphic (you can find similar structures between numbers in the range 1 - 100, and 1 million - 100million, or any arbitrary range) structures in the set that allows for easy inverse operations.

Finite fields resist inverse operations because they are not monotonic. 

Lets take f(x) = 2x. , where x =3 This naturally equals 6
But now lets say you have a field:  

*F_n = {0,1,2,3,4}*

(F_n just means field of n)

To keep the result of f(x) = 2x bounded in the field, we need mod 5. 
f(x) = 2x mod 5. So when we plug in 3, we get 1. 

*2(3) = 6*

*6 mod 5 = 1*

This is a demonstration of the non-monotonic nature of the field.

So why does a finite field resist inverse operations? While the finite field does have an exploitable structure, unless you use index calculus, generic algorithms still face O(√p) hardness. We will discuss index calculus when we talk about why we use an elliptic curve.

This is because the modulo operation destroys information about the history of the operation. 
Lets take 2^5 in R. 

*2^5 = 32*

Lets take 2^5 in our finite field F. 

*2^5 = 32*
-
*32 mod 5 = 2*

So what information did we lose? Well, the result "2" could have come from any of these exponentiation functions.

2^5
2^9
2^13

In R, the answer 32 contained implicit information about the exponent 5, but in our field, we only see the remainder 2.

This is the important concept known as the discrete log problem.

--------------------------------------------------

#THE CURVE

Before we can talk about the curve, we need to talk about fields and groups.
A field is a set of numbers that has two binary operations (*Addition and Multiplication*) that interact via the distributive law. As well as satisfying roughly 9-11 axioms, among which include: 

Closure: The operation stays inside the set.
Associativity: (A+B) + C = A + (B + C) 
Identity: There is a 0 element that does nothing.
Inverses: Every element has an inverse that cancels it. 
Distributivity: multiplication distributes over addition.

It should be noted, these axioms apply to both operations, plus additional requirements for how they interact

A group on the other hand is a set that has only one operation, either addition or multiplication, but not both. A group follows these 4 axioms:

-Closure: The operation stays inside the set.
-Associativity: (A+B) + C = A + (B + C) 
-Identity: There is an identity element e such that for any element a, a ⊕ e = a (where ⊕ is the group operation). For additive notation this is 0; for multiplicative notation this is 1."
-Inverses: Every element has an inverse that cancels it. 

Now lets talk about the curve in ECDH, why do we use a curve?
Well to start, an elliptic curve over a finite field is defined by a function that might look like:

*(y^2 ≡ x^3 + ax + b) mod p*

#IMPORTANT DETAIL

Well why cant we just use the finite prime field? Why do we care about the group defined by our elliptic curve? 

This is an important detail, pay close attention here:

Our field, in this case is a set of numbers: F_p = {0,1,2,3,..., p-1}
The crucial detail here is that factorization is possible for integers in (F_p)*, which index calculus exploits. So what do we do?

First we find the cartesian product of our field.
F_p x F_p = all possible coordinate pairs in our field. Lets call this set V.

However, there are no meaningful operations we can make on this set of coordinate pairs. (This is why its not a field) There is no single operation that works well for all them. This is where our equation comes in.

It defines a subset of our set V that has one well defined operation we can use, in this case it is point addition. 

The equation *(y^2 ≡ x^3 + ax + b) mod p* both selects which pairs are valid (those satisfying the equation) and defines how to add them geometrically

But why go to all this trouble? Well here is the beautiful part:

*Pairs have no factorization concept, and therefore it defeats index calculus.*

But why don't these pairs factorize I hear you ask?
It is because while integers have multiplicative structure, the points on our curve only have addition as their group operation (point addition.)
There's no meaningful way to "multiply" two points to get a third point. You can only add them.

Now we have an excellent trapdoor function: scalar multiplication (kP) is easy to compute forward, but the discrete log problem (finding k given P and kP) is extremely difficult to reverse


