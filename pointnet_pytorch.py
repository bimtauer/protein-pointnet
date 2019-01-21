class PointNet(nn.Module):
    def __init__(self, n_in, n_out):
        super().__init__()

        # input_Transformation_net
        self.input_Transformation_net == nn.sequential(
            nn.Conv1d(64),
            nn.ReLU(),
            nn.BatchNorm1d(),
            nn.Conv1d(128),
            nn.ReLU(),
            nn.BatchNorm1d(),
            nn.Conv1d(1024),
            nn.ReLU(),
            nn.BatchNorm1d(),
            nn.MaxPool1D()


        )



    def forward(self, x):
        x = self.fc(x)
        #x = self.si(x)
        return x#nn.functional.relu(x) #self.fc(x)# x#self.re(self.fc(x))

def custom_weights(m):
    if type(m) == nn.Linear:
        #torch.nn.init.xavier_uniform_(m.weight)
        #torch.nn.init.constant_(m.weight,0.2)
        m.weight.data.fill_(0.)
        m.bias.data.fill_(0.05)
