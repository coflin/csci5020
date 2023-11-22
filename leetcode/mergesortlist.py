class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        for num in nums2:
            nums1[m] = num
            m+=1
        print(sorted(nums1))

nums1=[0]
nums2=[1]
m = 0
n = 1
s = Solution()
s.merge(nums1,m,nums2,n)
