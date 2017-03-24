'''
The MIT License (MIT)

Copyright (c) 2015 Derek Willian Stavis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

class CPF(object):
    LEN_CORRECT_CPF = 11

    VALIDATION_FORMAT_STR = "{{:0{}}}".format(LEN_CORRECT_CPF)
    REPR_FORMAT_STR = "'{}({})'"
    STR_FORMAT_STR = "{}.{}.{}-{}"

    def __init__(self, cpf):
        self.cpf = cpf

    def __format__(self, format_spec=STR_FORMAT_STR):
        return format_spec.format(
            self.cpf[:3],
            self.cpf[3:6],
            self.cpf[6:9],
            self.cpf[9:]
        )

    @staticmethod
    def validate_cpf(cpf):
        """
        Checks if some CPF is valid.

        Reference: https://pt.wikipedia.org/wiki/Cadastro_de_pessoas_físicas

        :param cpf: CPF string containing just numbers
        :return: True if CPF is valid, False otherwise
        """

        len_diff = CPF.LEN_CORRECT_CPF - len(cpf)
        if len_diff > 0:
            cpf = CPF.VALIDATION_FORMAT_STR.format(int(cpf))

        fun_verifier1 = lambda x: x
        fun_verifier2 = lambda x: x + 1

        def calc_verifier(fun_v):
            return sum(
                map(
                    lambda v: int(v[1]) * (9 - (fun_v(v[0]) % 10)),
                    enumerate(reversed(cpf[:-2]))
                )
            )

        verifier_1 = calc_verifier(fun_verifier1)
        verifier_2 = calc_verifier(fun_verifier2)

        verifier_1 = (verifier_1 % 11) % 10

        verifier_2 += verifier_1 * 9
        verifier_2 = (verifier_2 % 11) % 10

        verifier_1_matches_last_but_one_digit = str(verifier_1) == cpf[-2]
        verifier_2_matches_last_digit = str(verifier_2) == cpf[-1]

        return verifier_1_matches_last_but_one_digit and verifier_2_matches_last_digit

    def validate(self):
        return self.validate_cpf(self.cpf)
