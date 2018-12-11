import string

poly = next(open('input')).strip()
print len(poly)

def reduce_poly(poly):
    found = True
    while found:
        i = 0
        found = False
        while i+1 < len(poly):
            c1 = poly[i]
            c2 = poly[i+1]
            if c1.lower() == c2.lower() and c1 != c2:
                assert len(poly[:i]) + len(poly[i+2:]) == len(poly) - 2
                poly = poly[:i] + poly[i+2:]
                found = True
            else:
                i += 1
    return poly

poly = reduce_poly(poly)
print len(poly)

new_lens = [len(reduce_poly(poly.replace(c, '').replace(c.upper(), ''))) for c in string.lowercase]

print min(new_lens)
