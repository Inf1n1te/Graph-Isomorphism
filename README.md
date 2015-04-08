# Graph-Isomorphism
MOD07 Project - Graph Isomorphism

The main program in our project is colorRefinement.py. In this file, at the very bottom we have our tests. You can uncomment whichever instance you want to test, or change the file location.
Without preprocessing the function to call is compare(<path>, <GI_only>). In this function <path> is a string that represents the path to the file you want to test which has to be a .grl-file. We recommend to put the file in the GI_TestInstancesWeek1 folder, but this is not required. The GI_only variable indicates if you want GI only. So if you put this on False, it will count isomorphisms, otherwise the amount of isomorphisms is not right, but it will do the isomorphic graph sets right.
With preprocessing the function to call is comparepreproc(<path>). In this function <path> is the same as in compare. This function will not count isomorhpisms (yet), because we did not have time to implement it.