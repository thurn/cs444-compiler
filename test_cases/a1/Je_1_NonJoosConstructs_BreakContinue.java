public class Je_1_NonJoosConstructs_BreakContinue {
  public int m(int x) {
    while (x>0) {
       x=x-1;
       if(x==10) continue;
       if (x==42) break;
    }
    return x;
  }
}

