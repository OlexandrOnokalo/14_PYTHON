# Конспект до фінальної співбесіди — RPA Developer

> Як користуватись: документ побудований так, щоб не треба було гуглити терміни під час читання. Кожен блок містить визначення, пояснення "чому це питають" і приклад коду (С#), де це доречно.

---

## 1. RPA — базові поняття

**Що таке RPA (Robotic Process Automation)** — технологія автоматизації рутинних, повторюваних, добре структурованих бізнес-процесів за допомогою програмних "роботів", які імітують дії людини в інтерфейсі: клікають, вводять текст, читають екран, працюють з файлами, веб-сторінками, API.

**Чим RPA відрізняється від звичайної автоматизації/скрипта:**
- RPA орієнтована на роботу через UI-рівень (як людина), коли немає прямого доступу до API системи (legacy-системи, веб-портали без API).
- RPA-рішення зазвичай мають стандартизовану архітектуру (init/process/end), логування, обробку винятків "з коробки" (або як прийнятий стандарт), механізми retry.
- Якщо є нормальний API — кращою практикою є інтеграція через API, а не через UI-автоматизацію (UI крихкий: змінився інтерфейс — бот ламається).

**Attended vs Unattended боти:**
- *Attended* — бот працює поруч з людиною, запускається людиною, допомагає в моменті (наприклад, кол-центр).
- *Unattended* — бот працює самостійно за розкладом/тригером, без участі людини (наприклад, нічна обробка замовлень — це наш кейс із тестового).

**Основні платформи RPA:**
- **UiPath** — найпопулярніша, своя IDE (Studio), Orchestrator для керування роботами, бібліотека активностей.
- **Power Automate (Microsoft)** — десктоп + хмарні флоу, інтеграція з Office 365.
- **Automation Anywhere, Blue Prism** — корпоративні аналоги.
- **Кастомні RPA-боти на коді** (C#, Python) — коли потрібна гнучкість, складна логіка, контроль над кодом, інтеграція з власною інфраструктурою; саме на це схожий стек вакансії (C# згадано знайомим).

**Чому це важливо знати:** навіть якщо компанія використовує конкретний інструмент (UiPath тощо), архітектурні принципи (нижче) однакові для будь-якої платформи.

### Архітектурний паттерн Init – Process – End (RE-Framework)

Це стандартний шаблон побудови RPA-процесу (в UiPath називається **ReFramework** — Robotic Enterprise Framework), і саме його логіку ти інтуїтивно відтворив у тестовому завданні.

1. **Initialization (Ініціалізація)**
   - Завантажити конфігурацію (шляхи, креди, налаштування).
   - Відкрити лог, перевірити середовище (наявність папок/файлів/з'єднань).
   - Залогінитись у системи (портал, CRM).
   - Якщо ініціалізація не вдалась — це **фатальна (System) помилка**, процес зупиняється повністю, бо без цих кроків подальша робота неможлива.

2. **Process (Головний цикл)**
   - Перебір елементів (transaction items) — у нашому випадку файли CSV, рядки в них.
   - Кожен елемент обробляється **незалежно**: якщо один впав з помилкою — переходимо до наступного, не зупиняючи весь процес (це ключова відмінність від звичайного "якщо помилка — крах програми").
   - Для кожного елемента: try → process → catch (записати помилку, позначити статус) → finally (перейти далі).

3. **End Process (Завершення)**
   - Закрити застосунки/сесії, зберегти фінальні звіти, лог, відправити сповіщення (якщо треба), звільнити ресурси.

**Чому тімлід може спитати:** "Чому ти переміщуєш файл в опрацьовані лише після успіху?", "Що як впаде бот посередині обробки файлу?" — відповідь будується саме на цьому паттерні: транзакційність на рівні одного елемента (файлу/рядка), а не всього процесу.

### Business Exception vs System (Application) Exception — важливий RPA-термін

- **Business Exception** — очікувана, "бізнесова" помилка: дані не відповідають правилам (немає обов'язкового поля, Client_ID не знайдено, портал повернув Unknown). Бот **не зупиняється**, фіксує в лог помилок і йде до наступного елемента. Це нормальна частина роботи бота.
- **System (Application) Exception** — технічна, непередбачена помилка: немає з'єднання з мережею, елемент UI не знайдено через зміну верстки, файл заблокований. Зазвичай застосовується **retry-логіка** (спробувати ще раз), і якщо retry не допомагає — або перехід до наступного елемента (якщо помилка локальна), або повна зупинка процесу (якщо помилка критична, як втрата сесії на порталі назавжди).

Це майже завжди питають на співбесідах з RPA — варто вміти чітко розділити ці два типи й навести приклад з твого тестового (Unknown статус — бізнес-кейс; портал недоступний — системний).

---

## 2. ООП + Паттерни проєктування

### 2.1 Чотири принципи ООП

1. **Інкапсуляція (Encapsulation)** — приховування внутрішньої реалізації об'єкта і надання доступу лише через публічний інтерфейс (властивості/методи). Захищає дані від некоректних змін ззовні.
   ```csharp
   public class Order
   {
       private decimal _price;
       public decimal Price
       {
           get => _price;
           set => _price = value >= 0 ? value : throw new ArgumentException("Price must be >= 0");
       }
   }
   ```

2. **Наслідування (Inheritance)** — клас-нащадок отримує поля й методи базового класу, може їх перевизначати. Дозволяє уникати дублювання коду.
   ```csharp
   public class FileProcessor { public virtual void Process() { } }
   public class CsvProcessor : FileProcessor
   {
       public override void Process() { /* специфічна логіка для CSV */ }
   }
   ```

3. **Поліморфізм (Polymorphism)** — можливість працювати з об'єктами різних класів через єдиний інтерфейс/базовий тип, при цьому кожен об'єкт поводиться по-своєму.
   - *Compile-time (overloading)* — кілька методів з однаковим іменем, різними параметрами.
   - *Runtime (overriding)* — виклик `virtual`/`override` методу визначається реальним типом об'єкта під час виконання.
   ```csharp
   List<FileProcessor> processors = new() { new CsvProcessor(), new ExcelProcessor() };
   foreach (var p in processors) p.Process(); // викликається відповідна реалізація
   ```

4. **Абстракція (Abstraction)** — виділення суттєвих характеристик об'єкта і приховування деталей реалізації; досягається через абстрактні класи й інтерфейси.

### 2.2 "На засипку" — типові каверзні питання

**Абстрактний клас vs Інтерфейс — ключова відмінність.**

| | Abstract class | Interface |
|---|---|---|
| Реалізація методів | Може містити і реалізовані, і абстрактні методи | До C# 8 — лише сигнатури; з C# 8+ можуть бути default-реалізації, але це менш типовий кейс |
| Поля | Може мати поля (стан) | Не може мати полів (тільки властивості/методи/події) |
| Множинне наслідування | Клас може наслідувати лише **один** абстрактний клас | Клас може реалізувати **багато** інтерфейсів |
| Конструктор | Може мати конструктор | Не може мати конструктор |
| Модифікатори доступу | Можуть бути будь-які (private, protected...) | Усі члени публічні за замовчуванням |
| Призначення | "Є" (is-a) відношення, спільна базова логіка для родини класів | "Може робити" (can-do) контракт поведінки, не пов'язаний ієрархією |

**Проста формула для відповіді на співбесіді:** "Абстрактний клас — це коли є спільна реалізація і спільний стан, які варто успадкувати. Інтерфейс — це коли потрібно гарантувати лише контракт (набір методів), без жодних зобов'язань щодо ієрархії чи реалізації, і коли клас має підтримувати кілька різних "ролей" одночасно."

**Інші питання "на засипку" з цієї теми:**

- *Чому в C# немає множинного наслідування класів, але є множинна реалізація інтерфейсів?* — щоб уникнути "Diamond Problem" (проблема алмазу): якщо два батьківські класи мають метод з однаковою сигнатурою й різною реалізацією — незрозуміло, яку викликати. Інтерфейси (до default-методів) цю проблему не створювали, бо не мали реалізації.

- *Що таке sealed клас?* — клас, який не можна успадкувати. Використовують для безпеки/оптимізації, коли подальше наслідування не передбачене.

- *Чим override відрізняється від new (модифікатор приховування)?* — `override` змінює поведінку віртуального методу для всіх викликів через базовий тип (поліморфізм зберігається); `new` просто "ховає" метод базового класу в похідному, і якщо звернутись через посилання на базовий тип — виклику ється базова версія (поліморфізм ламається).

- *Композиція vs наслідування (favor composition over inheritance) —* чому часто радять композицію: наслідування створює жорсткий зв'язок "is-a" і при зміні базового класу можуть зламатись усі нащадки (fragile base class problem); композиція ("has-a", об'єкт містить інший об'єкт як поле) — гнучкіша, легше тестувати й змінювати поведінку без перебудови ієрархії.

- *Чи можна створити екземпляр абстрактного класу?* — Ні, лише через нащадка. Але можна мати посилання типу абстрактного класу, що вказує на об'єкт нащадка.

- *Що таке virtual метод, якщо його не перевизначити в нащадку?* — викликається реалізація з базового класу (можна перевизначити, але не обов'язково — на відміну від абстрактного методу, який зобов'язаний бути реалізований).

- *Структура (struct) vs клас (class)* — struct — value type (копіюється при передачі, живе на стеку або всередині іншого об'єкта), class — reference type (копіюється посилання, живе в купі/heap). Struct не підтримує наслідування (окрім інтерфейсів), не має деструктора, частіше використовується для маленьких незмінних об'єктів (наприклад, координати, гроші).

### 2.3 SOLID — 5 принципів

**S — Single Responsibility Principle (Принцип єдиної відповідальності)**
Клас має мати лише одну причину для зміни — тобто відповідати за одну задачу.
```csharp
// Погано: клас і читає файл, і валідує, і пише в БД
public class OrderProcessor
{
    public void ReadCsv() {}
    public void ValidateOrder() {}
    public void SaveToDatabase() {}
}

// Добре: розділені відповідальності
public class CsvReader { public List<Order> Read(string path) => ...; }
public class OrderValidator { public bool Validate(Order o) => ...; }
public class OrderRepository { public void Save(Order o) {} }
```
*Чому важливо для RPA:* клас, який одночасно читає CSV, ходить на портал і пише в Excel — неможливо протестувати окремо й важко підтримувати.

**O — Open/Closed Principle (Принцип відкритості/закритості)**
Класи мають бути відкриті для розширення, але закриті для модифікації. Нову поведінку додаємо через наслідування/інтерфейси, не змінюючи існуючий код.
```csharp
public interface ICreditStatusProvider { string GetStatus(string clientId); }

public class WebPortalCreditProvider : ICreditStatusProvider
{
    public string GetStatus(string clientId) { /* парсинг веб-порталу */ return "Good"; }
}

// Якщо завтра з'явиться API замість порталу - додаємо новий клас, не чіпаючи старий
public class ApiCreditProvider : ICreditStatusProvider
{
    public string GetStatus(string clientId) { /* запит до REST API */ return "Good"; }
}
```

**L — Liskov Substitution Principle (Принцип підстановки Лісков)**
Об'єкт похідного класу повинен можна підставити замість об'єкта базового класу без порушення коректності програми.
```csharp
// Порушення LSP: Square "псує" поведінку Rectangle
public class Rectangle { public virtual int Width { get; set; } public virtual int Height { get; set; } }
public class Square : Rectangle
{
    public override int Width { set { base.Width = base.Height = value; } }
    // Якщо код очікує, що зміна Width не впливає на Height (як у Rectangle) - тут це порушується
}
```
*Простими словами:* якщо функція приймає базовий тип, заміна на будь-який підтип не повинна "ламати" логіку чи давати несподівану поведінку.

**I — Interface Segregation Principle (Принцип розділення інтерфейсів)**
Краще мати кілька маленьких специфічних інтерфейсів, ніж один великий "інтерфейс на все", щоб класи не змушені були реалізовувати методи, які їм не потрібні.
```csharp
// Погано
public interface IWorker { void Process(); void GenerateReport(); void SendEmail(); }

// Добре
public interface IProcessor { void Process(); }
public interface IReportGenerator { void GenerateReport(); }
public interface INotifier { void SendEmail(); }
```

**D — Dependency Inversion Principle (Принцип інверсії залежностей)**
Модулі високого рівня не повинні залежати від модулів низького рівня напряму — обидва повинні залежати від абстракцій (інтерфейсів).
```csharp
// Погано: OrderService напряму створює конкретну залежність
public class OrderService
{
    private readonly SqlOrderRepository _repo = new SqlOrderRepository(); // жорстка прив'язка
}

// Добре: залежність від абстракції, передається через конструктор
public class OrderService
{
    private readonly IOrderRepository _repo;
    public OrderService(IOrderRepository repo) => _repo = repo; // легко підмінити на Mock у тестах
}
```

### 2.4 Dependency Injection (DI)

**Що це:** техніка, коли об'єкт отримує свої залежності (інші об'єкти, від яких він залежить) **ззовні** (через конструктор, властивість або метод), а не створює їх сам усередині. Це конкретна реалізація принципу Dependency Inversion.

**Типи інжекції:**
1. **Constructor Injection** (найпоширеніший, рекомендований) — залежності передаються через конструктор.
2. **Property Injection** — залежність встановлюється через публічну властивість після створення об'єкта.
3. **Method Injection** — залежність передається як параметр конкретного методу, коли вона потрібна лише там.

**Навіщо DI:**
- Полегшує unit-тестування (можна підставити mock-об'єкт замість реальної залежності).
- Зменшує зв'язаність (coupling) між класами.
- Дозволяє змінювати реалізацію без зміни коду, що її використовує (наприклад, перейти з логування у файл на логування в БД).

**DI Container (IoC-контейнер):** спеціальний механізм, який сам створює об'єкти і "вприскує" потрібні залежності, керуючи їхнім життєвим циклом. У ASP.NET Core є вбудований контейнер.

**Lifetime (життєвий цикл) сервісів в ASP.NET Core:**
- **Transient** — новий екземпляр при кожному запиті залежності.
- **Scoped** — один екземпляр на один HTTP-запит (або одну "сесію обробки").
- **Singleton** — один екземпляр на весь час життя застосунку.

```csharp
// Реєстрація в Program.cs
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddSingleton<ILogger, FileLogger>();
builder.Services.AddTransient<ICreditStatusProvider, WebPortalCreditProvider>();

// Використання через конструктор
public class OrdersController : ControllerBase
{
    private readonly IOrderRepository _repo;
    public OrdersController(IOrderRepository repo) => _repo = repo; // контейнер сам підставить реалізацію
}
```
*Зв'язок з твоїм резюме:* у проєкті Cars API в тебе вже є ASP.NET Identity + JWT + Quartz — там DI використовується "з коробки", можна сказати, що ти з цим практично працював, навіть не завжди це усвідомлюючи як окрему тему.

### 2.5 Інші паттерни проєктування, які варто знати

**Repository Pattern** — абстрагує доступ до даних (БД, файл, API) за єдиним інтерфейсом, приховуючи деталі зберігання від бізнес-логіки.
```csharp
public interface IOrderRepository
{
    void Save(Order order);
    Order GetById(int id);
}
```

**Singleton** — гарантує, що клас має лише один екземпляр на весь застосунок, і надає глобальну точку доступу до нього. Приклад: об'єкт конфігурації, логер.
```csharp
public sealed class ConfigManager
{
    private static readonly ConfigManager _instance = new();
    public static ConfigManager Instance => _instance;
    private ConfigManager() { }
}
```

**Factory Method** — делегує створення об'єктів окремому методу/класу замість прямого виклику `new`, що дозволяє створювати об'єкти потрібного типу без зміни клієнтського коду.
```csharp
public interface IFileProcessor { void Process(string path); }
public static class FileProcessorFactory
{
    public static IFileProcessor Create(string extension) => extension switch
    {
        ".csv" => new CsvProcessor(),
        ".xlsx" => new ExcelProcessor(),
        _ => throw new NotSupportedException()
    };
}
```

**Strategy** — визначає сімейство алгоритмів, інкапсулює кожен в окремий клас і робить їх взаємозамінними під час виконання. Дуже доречний для RPA: наприклад, стратегія обробки помилки (retry / skip / escalate) може обиратись динамічно.
```csharp
public interface IRetryStrategy { void Execute(Action action); }
public class FixedDelayRetry : IRetryStrategy
{
    public void Execute(Action action)
    {
        for (int i = 0; i < 3; i++)
        {
            try { action(); return; }
            catch when (i < 2) { Thread.Sleep(30000); }
        }
    }
}
```

**Decorator** — динамічно "обгортає" об'єкт додатковою поведінкою без зміни його коду (наприклад, додати логування навколо викликів API).

**Observer** — об'єкт ("subject") сповіщає список залежних об'єктів ("observers") про зміни свого стану (основа подій/делегатів у C#, ASP.NET events).

---

## 3. Regex (регулярні вирази)

**Що це:** мова шаблонів для пошуку, перевірки й заміни тексту за певними правилами. У RPA активно використовується для валідації даних (формат email, телефону, кодів) і для парсингу неструктурованого тексту (наприклад, вирізати число з рядка "Сума: 1500.00 грн").

### Базовий синтаксис

| Символ | Значення | Приклад |
|---|---|---|
| `.` | будь-який символ (крім нового рядка) | `a.c` → "abc", "axc" |
| `^` | початок рядка | `^Hello` |
| `$` | кінець рядка | `world$` |
| `*` | 0 або більше повторень | `ab*` → "a", "ab", "abbb" |
| `+` | 1 або більше повторень | `ab+` → "ab", "abb" (не "a") |
| `?` | 0 або 1 раз (опціональність) | `colou?r` → "color", "colour" |
| `{n,m}` | від n до m повторень | `\d{2,4}` |
| `[]` | клас символів (один із перелічених) | `[abc]`, `[a-z]`, `[0-9]` |
| `[^]` | заперечення класу | `[^0-9]` — все, крім цифр |
| `\d` | цифра (0-9) | |
| `\D` | не цифра | |
| `\w` | слово-символ (букви, цифри, `_`) | |
| `\W` | не слово-символ | |
| `\s` | пробільний символ (пробіл, таб, новий рядок) | |
| `\S` | не пробільний символ | |
| `()`  | групування (та захоплення підрядка) | `(abc)+` |
| `(?:...)` | групування без захоплення | |
| `\|`  | "або" (альтернатива) | `cat\|dog` |
| `\b` | межа слова | `\bcat\b` не знайде "category" |

### Приклади під RPA-задачі

```csharp
using System.Text.RegularExpressions;

// Перевірка формату email
bool isValidEmail = Regex.IsMatch(input, @"^[\w\.-]+@[\w\.-]+\.\w{2,}$");

// Перевірка українського номера телефону
bool isValidPhone = Regex.IsMatch(input, @"^\+380\d{9}$");

// Витягнути всі коди товарів виду PROMO_XXX з рядка
var matches = Regex.Matches(text, @"PROMO_\d{3}");
foreach (Match m in matches) Console.WriteLine(m.Value);

// Перевірка, чи Client_ID складається лише з цифр і має 6-10 символів
bool isValidClientId = Regex.IsMatch(clientId, @"^\d{6,10}$");

// Заміна: видалити всі пробіли
string clean = Regex.Replace(input, @"\s+", "");

// Витягнути число з рядка "Сума: 1500.00 грн" через групу захоплення
var match = Regex.Match(text, @"Сума:\s*(\d+\.\d{2})");
if (match.Success) decimal amount = decimal.Parse(match.Groups[1].Value);
```

**Основні методи класу `Regex` (System.Text.RegularExpressions):**
- `Regex.IsMatch(input, pattern)` — повертає true/false, чи відповідає рядок шаблону.
- `Regex.Match(input, pattern)` — повертає перше знайдене співпадіння (`Match`).
- `Regex.Matches(input, pattern)` — повертає всі співпадіння.
- `Regex.Replace(input, pattern, replacement)` — заміна за шаблоном.
- `Regex.Split(input, pattern)` — розбиття рядка за шаблоном.

**Корисно знати:** компіляція регулярного виразу заздалегідь (`RegexOptions.Compiled`) пришвидшує повторне використання того самого шаблону у циклі (актуально для обробки великих CSV).

---

## 4. Робота з файлами

### 4.1 System.IO — основні класи

- **`File`** — статичні методи для роботи з файлами цілком: `File.Exists`, `File.ReadAllText`, `File.WriteAllLines`, `File.Copy`, `File.Move`, `File.Delete`.
- **`Directory`** — робота з папками: `Directory.Exists`, `Directory.CreateDirectory`, `Directory.GetFiles`, `Directory.GetDirectories`.
- **`Path`** — робота зі шляхами без звернення до диска: `Path.Combine`, `Path.GetFileName`, `Path.GetExtension`, `Path.GetDirectoryName`.
- **`FileInfo` / `DirectoryInfo`** — об'єктно-орієнтовані аналоги File/Directory, корисні, коли потрібно багато операцій з одним об'єктом (менше звернень до диска).
- **`Stream`, `FileStream`, `StreamReader`, `StreamWriter`** — потокове читання/запис, ефективніше для великих файлів, ніж `File.ReadAllText`.

```csharp
// Перевірка наявності папки і файлів (прямо з логіки твого тестового)
if (!Directory.Exists(folderPath))
{
    LogError("Папка не знайдена: " + folderPath);
    return;
}

string[] csvFiles = Directory.GetFiles(folderPath, "*.csv");
if (csvFiles.Length == 0)
{
    LogError("CSV файли не знайдено");
    return;
}

string processedFolder = Path.Combine(folderPath, "опрацьовані");
Directory.CreateDirectory(processedFolder); // не кидає помилку, якщо вже існує

foreach (var file in csvFiles)
{
    try
    {
        var lines = File.ReadAllLines(file);
        // ... обробка ...
        string destination = Path.Combine(processedFolder, Path.GetFileName(file));
        File.Move(file, destination);
    }
    catch (Exception ex)
    {
        LogError($"Помилка обробки файлу {file}: {ex.Message}");
    }
}
```

### 4.2 Парсинг CSV

```csharp
foreach (var line in File.ReadLines(csvPath).Skip(1)) // Skip(1) - пропустити заголовок
{
    var fields = line.Split(',');
    string productCode = fields[0];
    string clientId = fields[1];
    string clientName = fields[2];
    int quantity = int.Parse(fields[3]);
    decimal price = decimal.Parse(fields[4], CultureInfo.InvariantCulture);
}
```
**Важливий нюанс:** ручний `Split(',')` ламається, якщо в полях є коми всередині значення (наприклад, в назві товару) або лапки. Для надійного парсингу краще використовувати готову бібліотеку, наприклад **CsvHelper** — вона коректно обробляє екранування, лапки, різні роздільники.

```csharp
using CsvHelper;
using (var reader = new StreamReader(csvPath))
using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
{
    var records = csv.GetRecords<OrderCsvRecord>().ToList();
}
```

### 4.3 Робота з Excel з коду

Дві популярні бібліотеки:
- **ClosedXML** — простіша, зручна для читання/запису .xlsx, активно підтримується.
- **EPPlus** — потужніша, але з версії 5+ потребує ліцензії для комерційного використання (NonCommercial для навчальних проєктів).

```csharp
using ClosedXML.Excel;

// Створення/доповнення Daily_Report.xlsx
bool fileExists = File.Exists(reportPath);
using var workbook = fileExists ? new XLWorkbook(reportPath) : new XLWorkbook();
var sheet = fileExists ? workbook.Worksheet(1) : workbook.Worksheets.Add("Report");

if (!fileExists)
{
    string[] headers = { "ProcessingDate", "Client_ID", "ClientName", "ProductName",
                          "Quantity", "Price", "Credit_Status", "Is_Priority", "Processing_Result" };
    for (int i = 0; i < headers.Length; i++)
        sheet.Cell(1, i + 1).Value = headers[i];
}

int nextRow = sheet.LastRowUsed()?.RowNumber() + 1 ?? 2;
sheet.Cell(nextRow, 1).Value = DateTime.Now;
sheet.Cell(nextRow, 2).Value = order.ClientId;
// ... інші колонки ...

workbook.SaveAs(reportPath);
```

### 4.4 Типові проблеми з файлами, про які можуть спитати

- **Файл заблокований іншим процесом** (наприклад, відкритий вручну в Excel) — спроба запису кидає `IOException`; рішення — retry з очікуванням або перевірка через `try/catch` із власною функцією `IsFileLocked`.
- **Гонка умов (race condition)** при паралельній обробці кількох файлів кількома процесами — потрібні механізми блокування (lock-файли, або обробка через черги, а не напряму з папки).
- **Кодування файлу** — CSV може бути в UTF-8, Windows-1251 тощо; неправильне визначення кодування дає "кракозябри" у кириличних даних. Вирішується явним зазначенням `Encoding` при читанні (`File.ReadAllLines(path, Encoding.UTF8)`).
- **Асинхронність:** для файлових I/O операцій варто використовувати асинхронні методи (`File.ReadAllTextAsync`, `File.WriteAllLinesAsync`), щоб не блокувати потік, особливо у застосунках з UI (WPF) — ти це вже робив у Mail Manager.

---

## 5. Робота з API

### 5.1 Основи REST

**REST (Representational State Transfer)** — архітектурний стиль побудови веб-сервісів, де ресурси ідентифікуються URL, а дії над ними виконуються через стандартні HTTP-методи.

| Метод | Призначення |
|---|---|
| `GET` | отримати дані (без побічних ефектів) |
| `POST` | створити новий ресурс |
| `PUT` | повністю оновити (замінити) ресурс |
| `PATCH` | частково оновити ресурс |
| `DELETE` | видалити ресурс |

### 5.2 HTTP-статус-коди (групи, які треба знати напам'ять)

- **2xx — успіх**: `200 OK`, `201 Created`, `204 No Content`
- **3xx — переадресація**: `301 Moved Permanently`, `302 Found`
- **4xx — помилка клієнта**: `400 Bad Request`, `401 Unauthorized` (немає/невалідна авторизація — саме цей код фігурує у твоєму тестовому), `403 Forbidden` (авторизований, але немає прав), `404 Not Found`, `409 Conflict`
- **5xx — помилка серверу**: `500 Internal Server Error`, `503 Service Unavailable`

### 5.3 HttpClient у C#

```csharp
public class OrdersApiClient
{
    private readonly HttpClient _httpClient;

    public OrdersApiClient(HttpClient httpClient) => _httpClient = httpClient;

    public async Task<string> GetCreditStatusAsync(string clientId)
    {
        var response = await _httpClient.GetAsync($"/api/clients/{clientId}/status");

        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            await ReauthorizeAsync();
            response = await _httpClient.GetAsync($"/api/clients/{clientId}/status");
        }

        response.EnsureSuccessStatusCode(); // кидає виняток, якщо не 2xx
        string json = await response.Content.ReadAsStringAsync();
        var result = JsonSerializer.Deserialize<CreditStatusResponse>(json);
        return result.Status;
    }
}
```

**Важливо: `HttpClient` рекомендується реєструвати через `IHttpClientFactory` / DI**, а не створювати `new HttpClient()` щоразу — інакше можна виснажити пул socket-з'єднань (відома проблема socket exhaustion).
```csharp
builder.Services.AddHttpClient<OrdersApiClient>(client =>
{
    client.BaseAddress = new Uri("https://orders.client.com");
});
```

### 5.4 Авторизація

- **Bearer Token / JWT (JSON Web Token)** — токен, що передається в заголовку `Authorization: Bearer <token>`; складається з трьох частин (header.payload.signature), підписаний секретним ключем — сервер може перевірити автентичність без звернення до БД щоразу.
- **Refresh Token Rotation** — короткоживучий access-токен + довгоживучий refresh-токен; коли access-токен протух, клієнт використовує refresh-токен, щоб отримати новий access-токен без повторного логіну паролем (це в тебе реалізовано в Cars API — гарний привід розповісти детальніше).
- **Basic Auth** — логін:пароль у base64 в заголовку, простіше, але менш безпечно.
- **API Key** — статичний ключ, що передається в заголовку або query-параметрі.

### 5.5 Серіалізація JSON

```csharp
using System.Text.Json;

// Серіалізація об'єкта в JSON-рядок
string json = JsonSerializer.Serialize(order);

// Десеріалізація JSON-рядка в об'єкт
var order = JsonSerializer.Deserialize<Order>(json);

// Налаштування (наприклад, ігнорувати регістр імен властивостей)
var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var order2 = JsonSerializer.Deserialize<Order>(json, options);
```
Альтернатива — бібліотека **Newtonsoft.Json (Json.NET)**, історично популярніша, з більшою гнучкістю налаштувань, але `System.Text.Json` — вбудована й швидша, стандарт у нових .NET проєктах.

---

## 6. Обробка винятків (Exceptions)

### 6.1 Базовий синтаксис

```csharp
try
{
    ProcessOrder(order);
}
catch (FileNotFoundException ex)
{
    LogError($"Файл не знайдено: {ex.Message}");
}
catch (HttpRequestException ex) when (ex.Message.Contains("timeout"))
{
    // catch-фільтр: спрацьовує лише якщо умова true
    RetryRequest();
}
catch (Exception ex)
{
    LogError($"Невідома помилка: {ex.Message}");
    throw; // повторний кидок (re-throw) зі збереженням стек-трейсу - якщо не можемо обробити тут
}
finally
{
    CloseConnection(); // виконується завжди - і при успіху, і при помилці
}
```

**Порядок catch-блоків важливий:** від найбільш специфічного типу винятку до найбільш загального (`Exception`), інакше компілятор видасть помилку (specific exception unreachable) або найбільш загальний блок "перехопить" усе раніше за спеціалізований.

### 6.2 Ієрархія винятків (основні класи)

```
System.Exception
 ├── System.SystemException
 │     ├── NullReferenceException
 │     ├── ArgumentException
 │     │     └── ArgumentNullException
 │     ├── InvalidOperationException
 │     ├── IndexOutOfRangeException
 │     ├── FormatException
 │     ├── IOException
 │     │     └── FileNotFoundException
 │     ├── TimeoutException
 │     └── NotSupportedException
 └── System.ApplicationException (історично для кастомних винятків, зараз рідко використовується)
```

### 6.3 Власні (custom) винятки

```csharp
public class CsvValidationException : Exception
{
    public string FileName { get; }
    public CsvValidationException(string fileName, string message) : base(message)
    {
        FileName = fileName;
    }
}

// Використання
if (!HasRequiredFields(row))
    throw new CsvValidationException(fileName, "Відсутнє обов'язкове поле Product_Code");
```
**Навіщо власні винятки:** дозволяють розрізняти типи помилок у коді (наприклад, відловлювати саме `CsvValidationException` окремо від мережевих помилок) і передавати додатковий контекст (ім'я файлу, код помилки) разом з повідомленням.

### 6.4 Best practices, про які можуть спитати

- **Не використовувати exceptions для звичайного контролю потоку** (наприклад, не кидати виняток, щоб перевірити, чи існує файл — для цього є `File.Exists`). Exceptions — для дійсно виняткових ситуацій, бо генерація стек-трейсу "дорога" по продуктивності.
- **`throw;` vs `throw ex;`** — `throw;` зберігає оригінальний стек-трейс (де сталась помилка), `throw ex;` перезаписує стек-трейс на поточне місце, через що складніше знайти першопричину. Завжди використовуй `throw;` при повторному кидку.
- **Не ловити `Exception` "мовчки"** (порожній catch-блок) — це приховує реальні проблеми; мінімум — логувати.
- **`using` / `IDisposable`** — для звільнення ресурсів (файли, з'єднання) краще використовувати `using`-блок замість ручного `try/finally` із `Close()`, бо `using` гарантує виклик `Dispose()` навіть при винятку.
  ```csharp
  using (var reader = new StreamReader(path)) { /* ... */ } // Dispose() викликається автоматично
  ```
- **Retry-паттерн** (саме з твого тестового — 3 спроби з очікуванням 30с):
  ```csharp
  int attempts = 0;
  bool success = false;
  while (attempts < 3 && !success)
  {
      try
      {
          PerformWebAction();
          success = true;
      }
      catch (Exception ex)
      {
          attempts++;
          LogError($"Спроба {attempts} невдала: {ex.Message}");
          if (attempts < 3) Thread.Sleep(30000);
      }
  }
  if (!success) { LogError("Усі спроби невдалі"); /* escalate */ }
  ```

---

## 7. Логування

### 7.1 Рівні логування (від найдетальнішого до найважливішого)

1. **Trace** — найдетальніша інформація, для глибокого дебагу (значення кожної змінної, кожен крок).
2. **Debug** — інформація для розробників під час налагодження.
3. **Information / Info** — загальний перебіг роботи ("Файл X успішно обробено", "Бот стартував").
4. **Warning** — щось пішло не за планом, але не критично (наприклад, Unknown статус клієнта).
5. **Error** — помилка, яка не дозволила завершити конкретну операцію (не вдалось обробити рядок/файл).
6. **Critical / Fatal** — критична помилка, через яку весь процес/застосунок не може продовжувати роботу.

### 7.2 Serilog (вже є у твоєму резюме — Cars API)

```csharp
using Serilog;

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .WriteTo.Console()
    .WriteTo.File("logs/bot-log-.txt", rollingInterval: RollingInterval.Day) // ротація логів по днях
    .Enrich.FromLogContext()
    .CreateLogger();

Log.Information("Бот стартував обробку папки {FolderPath}", folderPath);
Log.Warning("Client {ClientId} отримав статус Unknown", clientId);
Log.Error(ex, "Помилка при обробці файлу {FileName}", fileName);
```

**Структуроване логування** (на відміну від простого `Console.WriteLine`) — кожне повідомлення містить іменовані параметри (`{ClientId}`), що дозволяє потім фільтрувати/шукати логи як структуровані дані (наприклад, у Seq, ElasticSearch, Application Insights), а не просто текстом.

### 7.3 Що логувати в RPA-боті (практичний чек-лист)

- Старт/завершення роботи бота, тривалість виконання.
- Кожен опрацьований елемент (файл, рядок) і результат (успіх/помилка).
- Усі бізнес-винятки (Unknown статус, відсутнє поле) — рівень Warning.
- Усі системні винятки (мережа, UI elements not found) — рівень Error, з повним stack trace.
- Спроби retry і їх результат.
- Підсумкову статистику в кінці (скільки всього/успішно/з помилками).
- **Не логувати чутливі дані** (паролі, повні номери карток, персональні дані без потреби) — про це теж можуть спитати в контексті безпеки/GDPR-подібних вимог.

### 7.4 Ротація і зберігання логів

- Ротація по днях/розміру файлу, щоб лог не "розростався" нескінченно.
- Зберігання N останніх днів/файлів (видалення старих автоматично).
- У production-середовищах часто виносять логи в централізовану систему (ELK stack, Application Insights, Seq), а не лишають лише локальні файли.


---

## 8. Бази даних (загально)

### 8.1 Реляційна модель

- **Таблиця (Table)** — набір рядків (записів) і колонок (полів) одного типу сутності.
- **Первинний ключ (Primary Key, PK)** — унікальний ідентифікатор рядка в таблиці; не може бути NULL, не повторюється.
- **Зовнішній ключ (Foreign Key, FK)** — поле, яке посилається на первинний ключ іншої таблиці, забезпечує зв'язок між таблицями і цілісність даних (referential integrity).
- **Типи зв'язків:**
  - **One-to-One (1:1)** — один запис пов'язаний рівно з одним записом іншої таблиці.
  - **One-to-Many (1:N)** — один запис пов'язаний з багатьма записами іншої таблиці (наприклад, один клієнт — багато замовлень).
  - **Many-to-Many (N:N)** — реалізується через промiжну (junction) таблицю з двома FK (наприклад, Flight ↔ Client у твоєму проєкті Airport).
- **Нормалізація** — процес структурування таблиць для уникнення дублювання даних і аномалій оновлення (1NF, 2NF, 3NF — нормальні форми, на базовому рівні достатньо розуміти суть: "кожен факт зберігається один раз").
- **Індекс (Index)** — структура даних, що прискорює пошук за певною колонкою (за рахунок додаткового місця й трохи повільнішого запису).
- **Транзакція (Transaction)** — набір операцій, які виконуються як єдине ціле: або всі успішно (commit), або жодна (rollback) — забезпечує властивості **ACID**:
  - **Atomicity** (атомарність) — все або нічого.
  - **Consistency** (узгодженість) — БД залишається у валідному стані до і після транзакції.
  - **Isolation** (ізольованість) — паралельні транзакції не впливають одна на одну некоректно.
  - **Durability** (стійкість) — після commit дані збережені навіть при збої системи.

### 8.2 Базовий SQL

```sql
-- Вибірка з умовою і сортуванням
SELECT ClientName, Quantity, Price
FROM Orders
WHERE CreditStatus = 'Good'
ORDER BY ProcessingDate DESC;

-- З'єднання таблиць (INNER JOIN - лише ті записи, що мають відповідність в обох таблицях)
SELECT o.ClientName, c.Email
FROM Orders o
INNER JOIN Clients c ON o.ClientId = c.Id;

-- LEFT JOIN - всі записи з лівої таблиці, навіть якщо немає відповідності в правій
SELECT c.ClientName, o.OrderId
FROM Clients c
LEFT JOIN Orders o ON c.Id = o.ClientId;

-- Групування й агрегація
SELECT CreditStatus, COUNT(*) AS Total, AVG(Price) AS AvgPrice
FROM Orders
GROUP BY CreditStatus
HAVING COUNT(*) > 5; -- HAVING фільтрує ГРУПИ (на відміну від WHERE, що фільтрує рядки до групування)

-- Вставка / оновлення / видалення
INSERT INTO Orders (ClientId, Quantity, Price) VALUES (101, 5, 250.00);
UPDATE Orders SET CreditStatus = 'Good' WHERE ClientId = 101;
DELETE FROM Orders WHERE ProcessingDate < '2024-01-01';
```

**Різниця `WHERE` і `HAVING`:** `WHERE` фільтрує окремі рядки до групування, `HAVING` фільтрує вже згруповані результати (наприклад, групи, де COUNT > 5).

### 8.3 ORM та Entity Framework Core (вже є в резюме)

**ORM (Object-Relational Mapping)** — технологія, що дозволяє працювати з БД через об'єкти мови програмування, а не писати SQL руками.

- **`DbContext`** — клас, що представляє сесію роботи з БД, містить `DbSet<T>` для кожної таблиці.
- **Code-First** — спочатку пишемо C#-класи (моделі), EF Core генерує з них схему БД через миграції.
- **Database-First** — спочатку є БД, з неї генеруються класи.
- **Миграції (Migrations)** — версійовані зміни схеми БД, що дозволяють еволюціонувати структуру таблиць разом з кодом (`Add-Migration`, `Update-Database`).
- **Fluent API** vs **Data Annotations** — два способи налаштувати схему: атрибутами над властивостями (`[Required]`, `[MaxLength(50)]`) або через `OnModelCreating` (більш гнучкий спосіб, який ти використовував у проєкті Airport).
- **LINQ (Language Integrated Query)** — спосіб писати запити до колекцій/БД безпосередньо в C#-синтаксисі:
  ```csharp
  var goodOrders = context.Orders
      .Where(o => o.CreditStatus == "Good")
      .OrderByDescending(o => o.ProcessingDate)
      .ToList();
  ```
- **Eager Loading (`.Include()`)** vs **Lazy Loading** — Eager одразу підвантажує пов'язані дані одним запитом (`context.Orders.Include(o => o.Client)`), Lazy підвантажує пов'язані дані лише в момент звернення до них (потребує додаткового налаштування й може призводити до проблеми "N+1 запитів", якщо не контролювати).
- **`SaveChanges()`** — застосовує всі накопичені зміни (insert/update/delete) в одній транзакції.

### 8.4 SQL Server vs PostgreSQL (короткий порівняльний штрих, раз обидва є в резюме)

Обидві — реляційні СУБД. SQL Server — продукт Microsoft, тісно інтегрований з .NET-екосистемою; PostgreSQL — відкритий, кросплатформовий, часто вважається більш стандартизованим щодо SQL і має потужні розширення (JSONB, GIS). У контексті EF Core різниця в основному в провайдері підключення (`Npgsql` для PostgreSQL).

---

## 9. Git-команди (широко)

### 9.1 Базові поняття

- **Repository (репозиторій)** — папка проєкту під контролем версій.
- **Commit** — знімок змін з повідомленням.
- **Branch (гілка)** — окрема лінія розробки.
- **Remote** — віддалений репозиторій (наприклад, GitHub).
- **HEAD** — вказівник на поточний коміт/гілку, де ти зараз перебуваєш.
- **Working directory / Staging area / Repository** — три "зони" Git: робочі файли → `git add` → індекс (staging) → `git commit` → історія.

### 9.2 Базові команди

```bash
git init                      # ініціалізувати новий репозиторій
git clone <url>                # скопіювати віддалений репозиторій локально
git status                     # показати стан робочої директорії та staging area
git add file.txt                # додати конкретний файл у staging area
git add .                       # додати всі змінені файли
git commit -m "повідомлення"    # зафіксувати зміни зі staging area
git commit -am "повідомлення"   # add + commit для вже трекованих файлів за один крок
git log                         # історія комітів
git log --oneline --graph       # компактна історія з графом гілок
git diff                        # показати незафіксовані зміни
git diff --staged               # показати зміни вже в staging area
```

### 9.3 Робота з гілками

```bash
git branch                      # список локальних гілок
git branch feature/new-bot       # створити нову гілку
git checkout feature/new-bot     # переключитись на гілку
git checkout -b feature/new-bot  # створити і одразу переключитись (скорочення)
git switch feature/new-bot       # сучасний аналог checkout для переключення гілок
git merge feature/new-bot        # злити гілку feature/new-bot у поточну
git branch -d feature/new-bot    # видалити локальну гілку (після злиття)
git branch -D feature/new-bot    # форсоване видалення (навіть незлита)
```

### 9.4 Робота з remote

```bash
git remote -v                          # показати список remote-репозиторіїв
git remote add origin <url>            # додати remote з назвою origin
git push origin main                    # відправити коміти на remote, гілка main
git push -u origin main                 # відправити і запам'ятати зв'язок гілки з remote (надалі просто git push)
git pull origin main                    # забрати + злити зміни з remote
git fetch origin                        # лише забрати зміни з remote, без автозлиття (безпечніше за pull)
```

### 9.5 Скасування і виправлення змін

```bash
git reset HEAD~1                # скасувати останній коміт, зберігши зміни у working directory
git reset --hard HEAD~1         # скасувати останній коміт ПОВНІСТЮ, втративши зміни (обережно!)
git revert <commit-hash>        # створити НОВИЙ коміт, що "відкатує" зміни попереднього (безпечно для публічної історії)
git stash                       # тимчасово відкласти незафіксовані зміни
git stash pop                   # повернути відкладені зміни назад
git checkout -- file.txt        # скасувати незафіксовані зміни в конкретному файлі
git restore file.txt             # сучасний аналог попередньої команди
```

### 9.6 Merge конфлікти

Виникають, коли дві гілки змінили один і той самий рядок файлу по-різному. Git позначає конфлікт прямо у файлі:
```
<<<<<<< HEAD
твій варіант коду
=======
варіант з гілки, яку зливаєш
>>>>>>> feature/new-bot
```
Треба вручну обрати/об'єднати потрібний варіант, видалити маркери `<<<<<<<`, `=======`, `>>>>>>>`, потім:
```bash
git add file.txt
git commit
```

**`git rebase` vs `git merge`:** `merge` створює новий "merge-коміт", що об'єднує дві гілки, зберігаючи повну історію розгалужень. `rebase` "переносить" коміти твоєї гілки на вершину іншої, формуючи лінійну (без розгалужень) історію — використовується для "чистоти" історії, але обережно: не рекомендується робити rebase на гілці, яку вже хтось інший використовує/спулив.

### 9.7 Інше корисне

```bash
git log -p file.txt              # історія змін конкретного файлу
git blame file.txt                # хто і коли змінював кожен рядок файлу
git tag v1.0.0                    # позначити версію (тег)
git cherry-pick <commit-hash>     # перенести один конкретний коміт в поточну гілку
.gitignore                        # файл зі списком файлів/папок, які Git ігнорує (наприклад, bin/, obj/, .vs/)
```

---

## 10. Linux-команди (коротко)

### 10.1 Навігація і файли

```bash
pwd                     # показати поточну директорію (print working directory)
ls                      # список файлів у поточній директорії
ls -la                  # список з прихованими файлами і деталями (права, розмір, дата)
cd /path/to/folder       # перейти в директорію
cd ..                    # піднятись на рівень вище
cd ~                     # перейти в домашню директорію
mkdir new_folder          # створити папку
rmdir empty_folder        # видалити ПОРОЖНЮ папку
rm file.txt               # видалити файл
rm -r folder              # видалити папку рекурсивно з усім вмістом
rm -rf folder              # те саме, але без підтвердження (обережно!)
cp source.txt dest.txt     # скопіювати файл
cp -r src_folder dest_folder  # скопіювати папку рекурсивно
mv old_name.txt new_name.txt  # перемістити/перейменувати файл
cat file.txt                # вивести вміст файлу в консоль
touch newfile.txt            # створити порожній файл / оновити час модифікації
nano file.txt / vim file.txt  # текстові редактори в консолі
```

### 10.2 Права доступу

```bash
chmod 755 script.sh        # змінити права доступу (rwx для власника, rx для групи й інших)
chmod +x script.sh         # додати право на виконання
chown user:group file.txt  # змінити власника файлу і групу
```
**Формат прав:** `r` (read=4), `w` (write=2), `x` (execute=1) — для трьох категорій: власник / група / інші. Наприклад `755` = власник rwx(7), група r-x(5), інші r-x(5).

### 10.3 Процеси і система

```bash
ps aux                  # список усіх процесів, що зараз виконуються
top                      # інтерактивний монітор процесів (CPU, RAM) у реальному часі
kill <PID>               # завершити процес за ID
kill -9 <PID>            # форсоване завершення процесу
df -h                     # використання дискового простору (human-readable)
du -sh folder             # розмір конкретної папки
```

### 10.4 Пошук і текстова обробка

```bash
grep "error" log.txt              # знайти рядки, що містять "error"
grep -r "error" /var/log           # рекурсивний пошук у всіх файлах папки
grep -i "error" log.txt            # пошук без урахування регістру
find /home -name "*.csv"            # знайти файли за іменем/шаблоном
echo "text" | grep "ex"             # пайп (передача виводу однієї команди як вхід для іншої)
cat file.txt | wc -l                 # підрахунок кількості рядків у файлі
command > output.txt                  # перенаправити вивід у файл (перезаписати)
command >> output.txt                 # перенаправити вивід у файл (додати в кінець)
```

### 10.5 Інше

```bash
sudo command            # виконати команду з правами адміністратора
man command              # відкрити довідку (manual) по команді
history                   # історія введених команд
which python              # показати шлях до виконуваного файлу команди
```


---

## 11. Розбір твого тестового завдання та проєктів із резюме

### 11.1 Питання, які можуть поставити по самому тестовому

**"Чому ти переміщуєш файл в опрацьовані лише ПІСЛЯ успішної обробки?"**
Відповідь: щоб забезпечити ідемпотентність процесу — якщо бот впаде посередині (наприклад, обірветься зв'язок), при наступному запуску файл все ще лежатиме в робочій папці і буде обробленим знову, а не "загубиться" як необроблений, але вже переміщений.

**"А що якщо файл впав з помилкою на 50-му з 100 рядків — що з уже обробленими 49?"**
Тут варто чесно визнати слабке місце твого алгоритму (це нормально на співбесіді — показує критичне мислення) і запропонувати покращення: записувати в CRM і звіт по кожному рядку одразу під час обробки (а не накопичувати в колекцію і писати все наприкінці файлу), щоб часткова обробка не губилась при падінні всередині файлу. Можна також згадати **checkpoint/transaction item rollback** — у класичному ReFramework кожен "transaction item" — окремий рядок, а не цілий файл, що дає більш гранулярну стійкість до збоїв.

**"Чому 3 спроби по 30 секунд, а не, наприклад, 5 по 10?"**
Чесна відповідь: це довільний параметр з умови завдання; в реальному проєкті такі значення зазвичай беруться з конфігураційного файлу (а не хардкодяться), щоб можна було підлаштовувати без перекомпіляції коду — і це гарна можливість показати, що ти розумієш важливість конфігурованості (можна згадати `appsettings.json` в .NET).

**"Як би ти обробляв 10 000 замовлень на день замість кількох файлів?"**
Тут доречно повторити те, що вже написано в розділі "Масштабування" твого тестового: Orchestrator, розбиття на Producer (читає файли, формує Queue) / Consumer (кілька паралельних роботів обробляють елементи черги), дашборд з метриками. Можна додати: обробка через **черги повідомлень** (наприклад, RabbitMQ, Azure Service Bus, або навіть просту БД-таблицю як черга) — кожен елемент бере один воркер, виключаючи дублювання обробки.

**"Як би ти тестував такого бота?"**
- Unit-тести для чистої бізнес-логіки (валідація PROMO_001, парсинг CSV) — без залежності від UI/мережі.
- Mock-об'єкти для зовнішніх залежностей (`ICreditStatusProvider` як інтерфейс — підставити фейкову реалізацію в тестах, що повертає наперед визначені статуси) — прямий зв'язок з DI/SOLID з розділу 2.
- Інтеграційні тести з тестовим середовищем (sandbox-портал, тестова БД) для перевірки наскрізного сценарію.

**"Чим відрізняється attended від unattended саме у твоєму процесі?"**
Описаний процес — типовий unattended-кейс: бот працює за розкладом (наприклад, щоночі) без участі людини, обробляючи всі файли самостійно.

### 11.2 Питання по твоїх .NET проєктах із резюме

- **Cars API:** "Як працює refresh token rotation?" — поясни механізм: при логіні видається пара access+refresh токен; коли access протух — клієнт відправляє refresh токен на спеціальний endpoint, сервер перевіряє його (валідність, чи не був уже використаний/відкликаний), видає нову пару токенів, **старий refresh токен інвалідується** (rotation — щоб уникнути повторного використання вкраденого токена). "Навіщо Quartz.NET для чищення токенів?" — фонове завдання за розкладом для видалення застарілих записів з БД, щоб таблиця не росла нескінченно.
- **Mail Manager:** "Як обробляються асинхронні операції в WPF, щоб UI не зависав?" — `async/await` для мережевих викликів (IMAP/SMTP), при цьому UI-потік (Dispatcher) лишається вільним для обробки подій інтерфейсу; типово блокуються елементи керування (`IsEnabled = false`) і показується wait cursor на час операції.
- **AWS S3 Manager:** "Як організована робота з потоками при upload/download?" — `Stream`-based I/O дозволяє не завантажувати весь файл у пам'ять одразу, а передавати його блоками, що ефективніше для великих файлів.
- **Airport Database:** "Як реалізовано Many-to-Many?" — через явну або неявну (з EF Core 5+ можна без проміжної сутності в коді, EF сам створить приховану таблицю) проміжну таблицю-зв'язку між Flight і Client.

### 11.3 Будь готовий чесно сказати, де "плаваєш"

Зважаючи на твою ситуацію (навчальні проєкти, півтора року практики, відсутність досвіду в RPA до тестового) — найкраща стратегія: **не намагатись вдавати глибоку експертизу там, де її немає**. Якщо питання виходить за межі того, що реально пам'ятаєш — краще сказати "я працював з цим у навчальному проєкті, основну ідею розумію, але детальні нюанси треба буде підняти/повторити" — це звучить чесно і професійно, і набагато краще за спробу "розмазати" відповідь, в якій тімлід відразу побачить прогалину.

---

## 12. Загальні та мотиваційні питання

Можливі питання і орієнтири для відповідей (не зазубрюй слово в слово — сформуй своїми словами на основі цих тез):

**"Чому RPA, якщо ти вчишся на .NET/Web-розробника?"**
Чесна відповідь, зважаючи на твою ситуацію: подався за рекомендацією знайомого, не знаючи деталей вакансії, до співбесіди не знав про існування RPA взагалі — але саме тестове завдання показало, що принципи (структуроване проєктування процесу, обробка винятків, логування, дизайн архітектури) дуже близькі до того, чим ти вже займаєшся в .NET-проєктах. RPA — це fullstack-подібна ніша, де C#-навички напряму застосовні, і це гарна можливість зайти в індустрію та нарощувати досвід "руками", паралельно поглиблюючи .NET.

**"Які твої сильні і слабкі сторони як кандидата?"**
- Сильні: аналітичне мислення (15+ років керування власним бізнесом і логістикою — вже звичка системно розкладати процес на кроки, саме це й видно в твоєму тестовому), швидке навчання нового (опанував кілька стеків за 1.5 року), технічний бекграунд з геодезії/GIS (звичка до точності й роботи з даними).
- Слабкі (і як їх компенсуєш): немає практичного досвіду в індустрії і конкретно в RPA — компенсуєш готовністю активно вчитись, структурованим підходом і чесністю щодо рівня знань (не вдаєш, що знаєш більше).

**"Як ти плануєш вивчати інструмент компанії (якщо це не чистий C#, а, наприклад, UiPath)?"**
Підготуй коротку відповідь типу: "Я готовий швидко зайти в інструмент через офіційну документацію й практику на тестових кейсах; базові інженерні принципи (паттерни, обробка помилок, логування) переносяться між будь-якими платформами — це я вже показав у тестовому завданні, описавши логіку без прив'язки до конкретного інструменту."

**"Чому саме ця компанія/вакансія?"**
Будь готовий чесно (але дипломатично) сформулювати: дізнався через знайомого, на етапі співбесіди розібрався в специфіці напрямку й бачиш, що це збігається з тим, чим хочеш розвиватись — структурована автоматизація бізнес-процесів на базі C#.

**Технічні "загальні" питання, які часто йдуть в кінці:**
- "Розкажи про свій останній проєкт" — підготуй короткий (2-3 хвилини) усний опис одного з проєктів резюме (рекомендую Cars API — найбільш комплексний) із наголосом на архітектурні рішення, а не лише на список технологій.
- "Які джерела ти використовуєш, щоб вчитись?" — документація Microsoft Learn, офіційні docs бібліотек, практика на власних проєктах.
- "Чи маєш питання до нас?" — підготуй заздалегідь 2-3 питання (наприклад: "Який стек використовується для RPA в компанії?", "Як виглядає типовий процес онбордингу і менторства для джуніора?", "Які проєкти/типи процесів я буду автоматизовувати на старті?") — це завжди справляє хороше враження і знімає частину невизначеності щодо самої роботи.

---

## Підсумкова шпаргалка (швидкий повтор перед співбесідою)

- **SOLID** — S(одна відповідальність) O(відкритий/закритий) L(підстановка Лісков) I(розділення інтерфейсів) D(інверсія залежностей).
- **Abstract class vs Interface** — клас: спільна реалізація+стан, одне наслідування; інтерфейс: лише контракт, множинна реалізація.
- **DI** — залежності передаються ззовні (через конструктор), а не створюються всередині класу; lifetime: Transient/Scoped/Singleton.
- **Business exception** — очікувана помилка даних, бот йде далі; **System exception** — технічна помилка, retry або зупинка.
- **Regex базові символи**: `\d \w \s . * + ? {} () [] ^ $ |`.
- **Файли**: `File`, `Directory`, `Path`; CSV — обережно з `Split(',')`, краще CsvHelper; Excel — ClosedXML/EPPlus.
- **API**: GET/POST/PUT/PATCH/DELETE; 401/403/404/500; JWT + Refresh token rotation; `HttpClient` через DI/IHttpClientFactory.
- **Exceptions**: `try/catch/finally`, `throw;` не `throw ex;`, власні класи винятків, retry-паттерн.
- **Логування**: Trace/Debug/Info/Warning/Error/Critical; Serilog; структуроване логування; не логувати чутливі дані.
- **БД**: PK/FK, 1:1/1:N/N:N, ACID, WHERE vs HAVING, EF Core (DbContext, миграції, LINQ, Include).
- **Git**: add/commit/push/pull/branch/merge/rebase/reset/revert/stash.
- **Linux**: ls/cd/cp/mv/rm/chmod/grep/find/ps/kill.
