import kotlin.math.*
import kotlin.random.Random

open class Poly {
    var order: Int
    var data: DoubleArray

    constructor(arr: DoubleArray) {
        data = trim(arr)
        order = data.size - 1
    }

    constructor() : this(doubleArrayOf(0.0))
    constructor(n: Int) : this(DoubleArray(n) { 0.0 })

    private fun trim(src: DoubleArray): DoubleArray {
        var deg = src.size - 1
        for (i in deg downTo 0) {
            if (src[i] == 0.0) deg-- else break
        }
        deg = max(deg, 0)
        return DoubleArray(deg + 1) { idx -> src[idx] }
    }

    fun d(): Poly {
        if (order == 0) return Poly(doubleArrayOf(0.0))

        val out = DoubleArray(order) { i -> data[i + 1] * (i + 1) }
        return Poly(out)
    }

    override fun toString(): String {
        val sb = StringBuilder()
        for (i in order downTo 0) {
            val c = data[i]
            if (c == 0.0) continue

            if (c > 0 && sb.isNotEmpty()) sb.append("+")
            if (c < 0) sb.append("-")

            sb.append(abs(c))
            if (i != 0) sb.append("*x^$i")
        }
        return sb.toString()
    }

    operator fun plus(other: Poly): Poly {
        val maxDeg = max(order, other.order)
        val result = DoubleArray(maxDeg + 1) { i ->
            val a = if (i <= order) data[i] else 0.0
            val b = if (i <= other.order) other.data[i] else 0.0
            a + b
        }
        return Poly(result)
    }

    operator fun times(k: Double): Poly =
        Poly(DoubleArray(order + 1) { i -> data[i] * k })

    operator fun Double.times(p: Poly) = p * this

    operator fun times(other: Poly): Poly {
        val out = DoubleArray(order + other.order + 1) { 0.0 }
        for (i in 0..order)
            for (j in 0..other.order)
                out[i + j] += data[i] * other.data[j]

        return Poly(out)
    }

    fun eval(x: Double): Double {
        var sum = 0.0
        for (i in 0..order) sum += data[i] * x.pow(i)
        return sum
    }
}


interface NodeSet {
    val xs: List<Double>
    var count: Int
}

data class UniformNodes(
    var left: Double,
    var right: Double,
    override var count: Int
) : NodeSet {
    override val xs: List<Double>
        get() {
            require(count > 2)
            require(left < right)

            return List(count) { i ->
                left + (right - left) * i / (count - 1)
            }
        }
}

data class RandNodes(
    override var count: Int,
    var lo: Double = 0.0,
    var hi: Double = 1.0
) : NodeSet {
    override val xs: List<Double>
        get() {
            require(count > 0)
            require(hi >= lo)
            return List(count) { Random.nextDouble(lo, hi) }.sorted()
        }
}

data class ChebNodes(
    override var count: Int,
    var l: Double = -1.0,
    var r: Double = 1.0
) : NodeSet {
    override val xs: List<Double>
        get() {
            require(count > 0)
            require(l <= r)

            return List(count) { k ->
                val base = -cos((2 * k + 1) * PI / (2 * count))
                (r - l) / 2 * base + (l + r) / 2
            }.sorted()
        }
}


class NewtonInterp {
    var pts: List<Double>
    var vals: List<Double>

    constructor(pts: List<Double>, vals: List<Double>) {
        this.pts = pts
        this.vals = vals
        check()
    }

    private fun check() {
        require(pts.size == vals.size)
        require(pts.toSet().size == pts.size)
    }

    private fun diffs(): DoubleArray {
        val zipped = pts.zip(vals).sortedBy { it.first }
        val xs = zipped.map { it.first }
        val ys = zipped.map { it.second }

        val n = xs.size
        val table = Array(n) { DoubleArray(n) }

        for (i in 0 until n) table[i][0] = ys[i]

        for (j in 1 until n) {
            for (i in 0 until n - j) {
                table[i][j] =
                    (table[i + 1][j - 1] - table[i][j - 1]) / (xs[i + j] - xs[i])
            }
        }

        return DoubleArray(n) { i -> table[0][i] }
    }

    fun poly(): Poly {
        val c = diffs()
        val sorted = pts.zip(vals).sortedBy { it.first }
        val xs = sorted.map { it.first }

        var p = Poly(doubleArrayOf(c[0]))

        for (i in 1 until xs.size) {
            var t = Poly(doubleArrayOf(c[i]))
            for (j in 0 until i) {
                t = t * Poly(doubleArrayOf(-xs[j], 1.0))
            }
            p += t
        }
        return p
    }

    fun valueAt(x: Double) = poly().eval(x)
}

// Примерные функции
fun f(x: Double) = 3 * x * x + 2 * x - 6
fun g(x: Double) = sin(x)
fun h(x: Double) = cos(x)

fun main() {
    val p = Poly(doubleArrayOf(7.0, 1.0, 2.0, 3.7)).also {
        println("P(x) = $it")
    }

    val dp = p.run {
        println("P'(x) = ${d()}")
        println("P(2) = ${eval(2.0)}\n")
        d()
    }

    val uni = UniformNodes(0.0, 2.0, 5)
    val cheb = ChebNodes(5, 0.0, 2.0)
    val rnd = RandNodes(5, 0.0, 2.0)

    println("Равномерные узлы: ${uni.xs}")
    println("Чебышевские узлы: ${cheb.xs}")
    println("Случайные узлы: ${rnd.xs}\n")

    val grid = listOf(0.0, 1.0, 2.0, 3.0, 4.0)
    val gridVals = grid.map { f(it) }

    val interp = NewtonInterp(grid, gridVals)

    println("Точки: $grid")
    println("F: $gridVals")

    val pol = interp.poly().also { println("Интерполянт: $it") }

    val xTest = 2.5
    println("Interp($xTest) = ${interp.valueAt(xTest)}")
    println("Exact f($xTest) = ${f(xTest)}\n")

    val sinPts = listOf(0.0, PI/4, PI/2, 3*PI/4, PI)
    val sinVals = sinPts.map { g(it) }
    val sinInterp = NewtonInterp(sinPts, sinVals)

    val sinPol = sinInterp.poly().also { println("sin-interp: $it") }
    println("sin-interp(pi/6) = ${sinInterp.valueAt(PI/6)}")
    println("sin(pi/6) = ${sin(PI/6)}\n")

    val cosPts = listOf(0.0, PI/4, PI/2, 3*PI/4, PI)
    val cosVals = cosPts.map { h(it) }
    val cosInterp = NewtonInterp(cosPts, cosVals)

    cosInterp.run {
        val cpol = poly()
        println("cos-interp: $cpol")
        val xx = PI / 6
        println("cos-interp(pi/6) = ${valueAt(xx)}")
        println("cos(pi/6) = ${cos(xx)}")
    }
}
