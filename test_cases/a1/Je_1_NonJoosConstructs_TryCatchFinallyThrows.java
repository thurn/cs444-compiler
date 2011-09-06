public class Je_1_NonJoosConstructs_TryCatchFinallyThrows {
  public int m(java.io.FileInputStream x) throws java.io.IOException{
    int y;
    try {
      y = x.read();
    } catch (java.io.IOException e) {
      y = 42;
    } finally {
      x.close();
    }
    return y;
  }
}

