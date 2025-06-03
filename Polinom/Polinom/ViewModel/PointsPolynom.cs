using System.Windows.Input;
using System.Windows.Media;
using System.Windows;
using System.ComponentModel;
using System.Collections.ObjectModel;
using Polinom.Model;


namespace Polinom.ViewModel
{
    class Circle : INotifyPropertyChanged
    {
        public double Radius { get; set; }

        private double _x;
        public double X { get => _x; set { _x = value; OnPropertyChanged(nameof(X)); } }

        private double _y;
        public double Y { get => _y; set { _y = value; OnPropertyChanged(nameof(Y)); } }

        public double Xr { get; set; }
        public double Yr { get; set; }


        public Circle(double x, double y)
        {
            Radius = 10;
            _x = x - Radius/2;
            _y = y - Radius/2;
            Xr = x;
            Yr = y;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    class MainViewModel : INotifyPropertyChanged
    {

        public ObservableCollection<Circle> Points { get; }

        private PointCollection _lagPoints;
        public PointCollection LagPoints
        {
            get => _lagPoints;
            set
            {
                if (_lagPoints == value) return;
                _lagPoints = value;
                OnPropertyChanged(nameof(LagPoints));
            }
        }

        public ICommand ClickCommand { get; }
        public ICommand ClickCreatePolynom {  get; }
        public ICommand ClickClear {  get; }

        private Polynom polynom;

        public MainViewModel()
        {
            Points = new ObservableCollection<Circle>();
            ClickCommand = new RelayCommand(obj => Create((Point)obj));
            ClickCreatePolynom = new RelayCommand(obj => CreatePolynom());
            ClickClear = new RelayCommand(obj => Clear());
        }

        private void Clear()
        {
            Points.Clear();
            LagPoints = new PointCollection();
        }

        private void Create(Point p)
        {
            var point = new Circle(p.X, p.Y);
            Points.Add(point);
        }

        public void CreatePolynom()
        {
            if (Points.Count < 2) return;
            var pts = Points.ToArray();
            var xValues = pts.Select(p => p.Xr).ToArray();
            var yValues = pts.Select(p => p.Yr).ToArray();

            double xMin = xValues.Min();
            double xMax = xValues.Max();
            double step = (xMax - xMin) / 300.0;
            var sampleX = new List<double>();
            for (double x = 0; x <= 800; x += step)
                sampleX.Add(x);
            foreach (var xi in xValues)
                if (!sampleX.Contains(xi))
                    sampleX.Add(xi);

            sampleX.Sort();

            var poly = new Polynom();
            LagPoints = new PointCollection();

            foreach (var x in sampleX)
            {
                double y = poly.Create(x, xValues, yValues, pts.Length);
                LagPoints.Add(new Point(x, y));
            }
        }

        public void Rebuild(double width, double height)
        {
            foreach (var point in Points)
            {
                point.X = point.Xr * width / 800 - point.Radius;
                point.Y = point.Yr * height / 400 - point.Radius;
            }
            OnPropertyChanged(nameof(Points));
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }


    public class RelayCommand : ICommand
    {
        private Action<object> execute;
        private Func<object, bool> canExecute;

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }

        public RelayCommand(Action<object> execute, Func<object, bool> canExecute = null)
        {
            this.execute = execute;
            this.canExecute = canExecute;
        }

        public bool CanExecute(object parameter)
        {
            return this.canExecute == null || this.canExecute(parameter);
        }

        public void Execute(object parameter)
        {
            this.execute(parameter);
        }
    }
}
