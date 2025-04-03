class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        # Convert the string to a list so we can modify it.
        s_list = list(s)

        # initialize two pointers left and right
        left = 0
        right = len(s_list)-1

        while left < right:
            # move left pointer until it points to a letter
            while left < right and not s_list[left].isalpha():
                left += 1
            # move the right pointer until it points to a letter
            while left < right and not s_list[right].isalpha():
                right -= 1

            s_list[left], s_list[right] = s_list[right], s_list[left]
            left += 1
            right -= 1

        return ''.join(s_list)
                
