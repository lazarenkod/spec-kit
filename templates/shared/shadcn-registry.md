# shadcn/ui Component Registry

Official component registry for shadcn/ui. Use this as the primary reference for component generation in `/speckit.design` and `/speckit.preview`.

**Source:** https://ui.shadcn.com/docs

---

## Quick Reference

| Category | Components |
|----------|------------|
| **Form** | Button, Input, Textarea, Checkbox, Radio Group, Select, Combobox, Toggle, Toggle Group, Switch, Slider, Input OTP, Label, Form |
| **Display** | Card, Badge, Alert, Avatar, Skeleton, Separator, Aspect Ratio, Scroll Area, Resizable, Collapsible |
| **Navigation** | Breadcrumb, Pagination, Menubar, Navigation Menu, Dropdown Menu, Context Menu, Tabs, Sidebar |
| **Overlays** | Dialog, Alert Dialog, Drawer, Popover, Hover Card, Tooltip, Sheet, Command |
| **Data** | Table, Data Table, Carousel, Calendar, Progress, Chart |
| **Feedback** | Spinner, Toast, Sonner |
| **Typography** | Typography (prose styles) |
| **Utility** | Kbd, Accordion |

---

## Styling Conventions

### Import Pattern
```typescript
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
```

### Variant System (CVA)
```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### cn() Utility
```typescript
// lib/utils.ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Form Components

### Button
**Import:** `@/components/ui/button`
**Dependencies:** `class-variance-authority`

| Variant | Description |
|---------|-------------|
| `default` | Primary button with solid background |
| `destructive` | Red/danger action button |
| `outline` | Border only, transparent background |
| `secondary` | Muted secondary action |
| `ghost` | No background, hover reveals |
| `link` | Styled as text link |

| Size | Dimensions |
|------|------------|
| `default` | h-9, px-4, py-2 |
| `sm` | h-8, px-3, text-xs |
| `lg` | h-10, px-8 |
| `icon` | h-9, w-9 (square) |

```tsx
<Button variant="default" size="default">Click me</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline" size="sm">Cancel</Button>
<Button variant="ghost" size="icon"><IconMenu /></Button>
```

### Input
**Import:** `@/components/ui/input`
**Dependencies:** None

```tsx
<Input type="email" placeholder="Email" />
<Input type="password" disabled />
<Input className="file:bg-transparent file:border-0" type="file" />
```

### Textarea
**Import:** `@/components/ui/textarea`
**Dependencies:** None

```tsx
<Textarea placeholder="Type your message here." />
<Textarea className="resize-none" rows={4} />
```

### Checkbox
**Import:** `@/components/ui/checkbox`
**Dependencies:** `@radix-ui/react-checkbox`

```tsx
<Checkbox id="terms" />
<label htmlFor="terms">Accept terms and conditions</label>

<Checkbox checked={checked} onCheckedChange={setChecked} />
```

### Radio Group
**Import:** `@/components/ui/radio-group`
**Dependencies:** `@radix-ui/react-radio-group`

```tsx
<RadioGroup defaultValue="option-one">
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="option-one" id="option-one" />
    <Label htmlFor="option-one">Option One</Label>
  </div>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="option-two" id="option-two" />
    <Label htmlFor="option-two">Option Two</Label>
  </div>
</RadioGroup>
```

### Select
**Import:** `@/components/ui/select`
**Dependencies:** `@radix-ui/react-select`

```tsx
<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectGroup>
      <SelectLabel>Fruits</SelectLabel>
      <SelectItem value="apple">Apple</SelectItem>
      <SelectItem value="banana">Banana</SelectItem>
      <SelectItem value="orange">Orange</SelectItem>
    </SelectGroup>
  </SelectContent>
</Select>
```

### Combobox
**Import:** `@/components/ui/command` + `@/components/ui/popover`
**Dependencies:** `@radix-ui/react-popover`, `cmdk`

```tsx
<Popover open={open} onOpenChange={setOpen}>
  <PopoverTrigger asChild>
    <Button variant="outline" role="combobox" aria-expanded={open}>
      {value ? frameworks.find((f) => f.value === value)?.label : "Select framework..."}
      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
    </Button>
  </PopoverTrigger>
  <PopoverContent className="w-[200px] p-0">
    <Command>
      <CommandInput placeholder="Search framework..." />
      <CommandList>
        <CommandEmpty>No framework found.</CommandEmpty>
        <CommandGroup>
          {frameworks.map((framework) => (
            <CommandItem key={framework.value} value={framework.value} onSelect={...}>
              {framework.label}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </Command>
  </PopoverContent>
</Popover>
```

### Toggle
**Import:** `@/components/ui/toggle`
**Dependencies:** `@radix-ui/react-toggle`

| Variant | Description |
|---------|-------------|
| `default` | Standard toggle |
| `outline` | Border toggle |

```tsx
<Toggle aria-label="Toggle bold">
  <Bold className="h-4 w-4" />
</Toggle>
<Toggle variant="outline" pressed={pressed} onPressedChange={setPressed}>
  <Italic className="h-4 w-4" />
</Toggle>
```

### Toggle Group
**Import:** `@/components/ui/toggle-group`
**Dependencies:** `@radix-ui/react-toggle-group`

```tsx
<ToggleGroup type="single" defaultValue="center">
  <ToggleGroupItem value="left" aria-label="Left aligned">
    <AlignLeft className="h-4 w-4" />
  </ToggleGroupItem>
  <ToggleGroupItem value="center" aria-label="Center aligned">
    <AlignCenter className="h-4 w-4" />
  </ToggleGroupItem>
  <ToggleGroupItem value="right" aria-label="Right aligned">
    <AlignRight className="h-4 w-4" />
  </ToggleGroupItem>
</ToggleGroup>
```

### Switch
**Import:** `@/components/ui/switch`
**Dependencies:** `@radix-ui/react-switch`

```tsx
<div className="flex items-center space-x-2">
  <Switch id="airplane-mode" />
  <Label htmlFor="airplane-mode">Airplane Mode</Label>
</div>
```

### Slider
**Import:** `@/components/ui/slider`
**Dependencies:** `@radix-ui/react-slider`

```tsx
<Slider defaultValue={[50]} max={100} step={1} />
<Slider defaultValue={[25, 75]} max={100} step={1} /> {/* Range */}
```

### Input OTP
**Import:** `@/components/ui/input-otp`
**Dependencies:** `input-otp`

```tsx
<InputOTP maxLength={6}>
  <InputOTPGroup>
    <InputOTPSlot index={0} />
    <InputOTPSlot index={1} />
    <InputOTPSlot index={2} />
  </InputOTPGroup>
  <InputOTPSeparator />
  <InputOTPGroup>
    <InputOTPSlot index={3} />
    <InputOTPSlot index={4} />
    <InputOTPSlot index={5} />
  </InputOTPGroup>
</InputOTP>
```

### Label
**Import:** `@/components/ui/label`
**Dependencies:** `@radix-ui/react-label`

```tsx
<Label htmlFor="email">Email</Label>
<Input type="email" id="email" placeholder="Email" />
```

### Form (React Hook Form)
**Import:** `@/components/ui/form`
**Dependencies:** `react-hook-form`, `@hookform/resolvers`, `zod`

```tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
    <FormField
      control={form.control}
      name="username"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Username</FormLabel>
          <FormControl>
            <Input placeholder="shadcn" {...field} />
          </FormControl>
          <FormDescription>This is your public display name.</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
    <Button type="submit">Submit</Button>
  </form>
</Form>
```

---

## Display Components

### Card
**Import:** `@/components/ui/card`
**Dependencies:** None

```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card Description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card Content</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Badge
**Import:** `@/components/ui/badge`
**Dependencies:** `class-variance-authority`

| Variant | Description |
|---------|-------------|
| `default` | Primary badge |
| `secondary` | Muted badge |
| `destructive` | Error/danger badge |
| `outline` | Border only |

```tsx
<Badge>Badge</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge variant="outline">Outline</Badge>
```

### Alert
**Import:** `@/components/ui/alert`
**Dependencies:** `class-variance-authority`

| Variant | Description |
|---------|-------------|
| `default` | Standard alert |
| `destructive` | Error alert |

```tsx
<Alert>
  <Terminal className="h-4 w-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components to your app using the cli.
  </AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Your session has expired.</AlertDescription>
</Alert>
```

### Avatar
**Import:** `@/components/ui/avatar`
**Dependencies:** `@radix-ui/react-avatar`

```tsx
<Avatar>
  <AvatarImage src="https://github.com/shadcn.png" alt="@shadcn" />
  <AvatarFallback>CN</AvatarFallback>
</Avatar>
```

### Skeleton
**Import:** `@/components/ui/skeleton`
**Dependencies:** None

```tsx
<div className="flex items-center space-x-4">
  <Skeleton className="h-12 w-12 rounded-full" />
  <div className="space-y-2">
    <Skeleton className="h-4 w-[250px]" />
    <Skeleton className="h-4 w-[200px]" />
  </div>
</div>
```

### Separator
**Import:** `@/components/ui/separator`
**Dependencies:** `@radix-ui/react-separator`

```tsx
<Separator />
<Separator orientation="vertical" className="h-4" />
```

### Aspect Ratio
**Import:** `@/components/ui/aspect-ratio`
**Dependencies:** `@radix-ui/react-aspect-ratio`

```tsx
<AspectRatio ratio={16 / 9} className="bg-muted">
  <Image src="..." alt="..." fill className="object-cover" />
</AspectRatio>
```

### Scroll Area
**Import:** `@/components/ui/scroll-area`
**Dependencies:** `@radix-ui/react-scroll-area`

```tsx
<ScrollArea className="h-72 w-48 rounded-md border">
  <div className="p-4">
    {tags.map((tag) => (
      <div key={tag} className="text-sm">{tag}</div>
    ))}
  </div>
</ScrollArea>
```

### Resizable
**Import:** `@/components/ui/resizable`
**Dependencies:** `react-resizable-panels`

```tsx
<ResizablePanelGroup direction="horizontal">
  <ResizablePanel defaultSize={50}>
    <div className="flex h-full items-center justify-center p-6">
      <span className="font-semibold">One</span>
    </div>
  </ResizablePanel>
  <ResizableHandle />
  <ResizablePanel defaultSize={50}>
    <div className="flex h-full items-center justify-center p-6">
      <span className="font-semibold">Two</span>
    </div>
  </ResizablePanel>
</ResizablePanelGroup>
```

### Collapsible
**Import:** `@/components/ui/collapsible`
**Dependencies:** `@radix-ui/react-collapsible`

```tsx
<Collapsible open={isOpen} onOpenChange={setIsOpen}>
  <CollapsibleTrigger asChild>
    <Button variant="ghost">Toggle</Button>
  </CollapsibleTrigger>
  <CollapsibleContent>
    <div className="rounded-md border px-4 py-3">Content here...</div>
  </CollapsibleContent>
</Collapsible>
```

---

## Navigation Components

### Breadcrumb
**Import:** `@/components/ui/breadcrumb`
**Dependencies:** None

```tsx
<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/components">Components</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>Breadcrumb</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>
```

### Pagination
**Import:** `@/components/ui/pagination`
**Dependencies:** None

```tsx
<Pagination>
  <PaginationContent>
    <PaginationItem>
      <PaginationPrevious href="#" />
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#">1</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#" isActive>2</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationEllipsis />
    </PaginationItem>
    <PaginationItem>
      <PaginationNext href="#" />
    </PaginationItem>
  </PaginationContent>
</Pagination>
```

### Menubar
**Import:** `@/components/ui/menubar`
**Dependencies:** `@radix-ui/react-menubar`

```tsx
<Menubar>
  <MenubarMenu>
    <MenubarTrigger>File</MenubarTrigger>
    <MenubarContent>
      <MenubarItem>New Tab <MenubarShortcut>⌘T</MenubarShortcut></MenubarItem>
      <MenubarItem>New Window</MenubarItem>
      <MenubarSeparator />
      <MenubarItem>Share</MenubarItem>
      <MenubarSeparator />
      <MenubarItem>Print</MenubarItem>
    </MenubarContent>
  </MenubarMenu>
</Menubar>
```

### Navigation Menu
**Import:** `@/components/ui/navigation-menu`
**Dependencies:** `@radix-ui/react-navigation-menu`

```tsx
<NavigationMenu>
  <NavigationMenuList>
    <NavigationMenuItem>
      <NavigationMenuTrigger>Getting started</NavigationMenuTrigger>
      <NavigationMenuContent>
        <ul className="grid gap-3 p-4 md:w-[400px]">
          <ListItem href="/docs" title="Introduction">
            Re-usable components built using Radix UI and Tailwind CSS.
          </ListItem>
        </ul>
      </NavigationMenuContent>
    </NavigationMenuItem>
  </NavigationMenuList>
</NavigationMenu>
```

### Dropdown Menu
**Import:** `@/components/ui/dropdown-menu`
**Dependencies:** `@radix-ui/react-dropdown-menu`

```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Open</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent className="w-56">
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuGroup>
      <DropdownMenuItem>Profile <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut></DropdownMenuItem>
      <DropdownMenuItem>Settings <DropdownMenuShortcut>⌘S</DropdownMenuShortcut></DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Log out <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut></DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### Context Menu
**Import:** `@/components/ui/context-menu`
**Dependencies:** `@radix-ui/react-context-menu`

```tsx
<ContextMenu>
  <ContextMenuTrigger className="flex h-[150px] w-[300px] items-center justify-center rounded-md border border-dashed">
    Right click here
  </ContextMenuTrigger>
  <ContextMenuContent className="w-64">
    <ContextMenuItem>Back <ContextMenuShortcut>⌘[</ContextMenuShortcut></ContextMenuItem>
    <ContextMenuItem>Forward <ContextMenuShortcut>⌘]</ContextMenuShortcut></ContextMenuItem>
    <ContextMenuSeparator />
    <ContextMenuSub>
      <ContextMenuSubTrigger>More Tools</ContextMenuSubTrigger>
      <ContextMenuSubContent className="w-48">
        <ContextMenuItem>Save Page As...</ContextMenuItem>
      </ContextMenuSubContent>
    </ContextMenuSub>
  </ContextMenuContent>
</ContextMenu>
```

### Tabs
**Import:** `@/components/ui/tabs`
**Dependencies:** `@radix-ui/react-tabs`

```tsx
<Tabs defaultValue="account" className="w-[400px]">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
  </TabsList>
  <TabsContent value="account">Account settings...</TabsContent>
  <TabsContent value="password">Password settings...</TabsContent>
</Tabs>
```

### Sidebar
**Import:** `@/components/ui/sidebar`
**Dependencies:** None (uses CSS variables for width)

```tsx
<SidebarProvider>
  <Sidebar>
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg">
            <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary">
              <GalleryVerticalEnd className="size-4 text-primary-foreground" />
            </div>
            <span className="font-semibold">Acme Inc</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Application</SidebarGroupLabel>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <a href="/dashboard"><LayoutDashboard className="size-4" /> Dashboard</a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter />
  </Sidebar>
  <SidebarInset>
    {/* Main content */}
  </SidebarInset>
</SidebarProvider>
```

---

## Overlay Components

### Dialog
**Import:** `@/components/ui/dialog`
**Dependencies:** `@radix-ui/react-dialog`

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here. Click save when done.
      </DialogDescription>
    </DialogHeader>
    <div className="grid gap-4 py-4">
      <Input id="name" defaultValue="Pedro Duarte" />
    </div>
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Alert Dialog
**Import:** `@/components/ui/alert-dialog`
**Dependencies:** `@radix-ui/react-alert-dialog`

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="outline">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Continue</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Drawer
**Import:** `@/components/ui/drawer`
**Dependencies:** `vaul`

```tsx
<Drawer>
  <DrawerTrigger asChild>
    <Button variant="outline">Open Drawer</Button>
  </DrawerTrigger>
  <DrawerContent>
    <DrawerHeader>
      <DrawerTitle>Edit profile</DrawerTitle>
      <DrawerDescription>Make changes to your profile.</DrawerDescription>
    </DrawerHeader>
    <div className="p-4">Drawer content here...</div>
    <DrawerFooter>
      <Button>Submit</Button>
      <DrawerClose asChild>
        <Button variant="outline">Cancel</Button>
      </DrawerClose>
    </DrawerFooter>
  </DrawerContent>
</Drawer>
```

### Sheet
**Import:** `@/components/ui/sheet`
**Dependencies:** `@radix-ui/react-dialog`

```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open</Button>
  </SheetTrigger>
  <SheetContent side="right">
    <SheetHeader>
      <SheetTitle>Edit profile</SheetTitle>
      <SheetDescription>Make changes to your profile.</SheetDescription>
    </SheetHeader>
    <div className="grid gap-4 py-4">
      {/* Content */}
    </div>
    <SheetFooter>
      <SheetClose asChild>
        <Button type="submit">Save changes</Button>
      </SheetClose>
    </SheetFooter>
  </SheetContent>
</Sheet>
```

### Popover
**Import:** `@/components/ui/popover`
**Dependencies:** `@radix-ui/react-popover`

```tsx
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">Open popover</Button>
  </PopoverTrigger>
  <PopoverContent className="w-80">
    <div className="grid gap-4">
      <div className="space-y-2">
        <h4 className="font-medium leading-none">Dimensions</h4>
        <p className="text-sm text-muted-foreground">Set dimensions.</p>
      </div>
    </div>
  </PopoverContent>
</Popover>
```

### Hover Card
**Import:** `@/components/ui/hover-card`
**Dependencies:** `@radix-ui/react-hover-card`

```tsx
<HoverCard>
  <HoverCardTrigger asChild>
    <Button variant="link">@nextjs</Button>
  </HoverCardTrigger>
  <HoverCardContent className="w-80">
    <div className="flex justify-between space-x-4">
      <Avatar>
        <AvatarImage src="https://github.com/vercel.png" />
        <AvatarFallback>VC</AvatarFallback>
      </Avatar>
      <div className="space-y-1">
        <h4 className="text-sm font-semibold">@nextjs</h4>
        <p className="text-sm">The React Framework.</p>
      </div>
    </div>
  </HoverCardContent>
</HoverCard>
```

### Tooltip
**Import:** `@/components/ui/tooltip`
**Dependencies:** `@radix-ui/react-tooltip`

```tsx
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger asChild>
      <Button variant="outline">Hover</Button>
    </TooltipTrigger>
    <TooltipContent>
      <p>Add to library</p>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

### Command
**Import:** `@/components/ui/command`
**Dependencies:** `cmdk`

```tsx
<Command className="rounded-lg border shadow-md">
  <CommandInput placeholder="Type a command or search..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Suggestions">
      <CommandItem>
        <Calendar className="mr-2 h-4 w-4" />
        <span>Calendar</span>
      </CommandItem>
      <CommandItem>
        <Smile className="mr-2 h-4 w-4" />
        <span>Search Emoji</span>
      </CommandItem>
    </CommandGroup>
    <CommandSeparator />
    <CommandGroup heading="Settings">
      <CommandItem>
        <User className="mr-2 h-4 w-4" />
        <span>Profile</span>
        <CommandShortcut>⌘P</CommandShortcut>
      </CommandItem>
    </CommandGroup>
  </CommandList>
</Command>
```

---

## Data Components

### Table
**Import:** `@/components/ui/table`
**Dependencies:** None

```tsx
<Table>
  <TableCaption>A list of your recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead className="w-[100px]">Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell className="font-medium">INV001</TableCell>
      <TableCell>Paid</TableCell>
      <TableCell>Credit Card</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
  </TableBody>
  <TableFooter>
    <TableRow>
      <TableCell colSpan={3}>Total</TableCell>
      <TableCell className="text-right">$2,500.00</TableCell>
    </TableRow>
  </TableFooter>
</Table>
```

### Data Table (TanStack Table)
**Import:** `@/components/ui/data-table`
**Dependencies:** `@tanstack/react-table`

```tsx
// columns.tsx
export const columns: ColumnDef<Payment>[] = [
  { accessorKey: "status", header: "Status" },
  { accessorKey: "email", header: "Email" },
  {
    accessorKey: "amount",
    header: () => <div className="text-right">Amount</div>,
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue("amount"))
      const formatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(amount)
      return <div className="text-right font-medium">{formatted}</div>
    },
  },
]

// page.tsx
<DataTable columns={columns} data={data} />
```

### Carousel
**Import:** `@/components/ui/carousel`
**Dependencies:** `embla-carousel-react`

```tsx
<Carousel className="w-full max-w-xs">
  <CarouselContent>
    {Array.from({ length: 5 }).map((_, index) => (
      <CarouselItem key={index}>
        <div className="p-1">
          <Card>
            <CardContent className="flex aspect-square items-center justify-center p-6">
              <span className="text-4xl font-semibold">{index + 1}</span>
            </CardContent>
          </Card>
        </div>
      </CarouselItem>
    ))}
  </CarouselContent>
  <CarouselPrevious />
  <CarouselNext />
</Carousel>
```

### Calendar
**Import:** `@/components/ui/calendar`
**Dependencies:** `react-day-picker`

```tsx
<Calendar
  mode="single"
  selected={date}
  onSelect={setDate}
  className="rounded-md border"
/>

<Calendar
  mode="range"
  selected={dateRange}
  onSelect={setDateRange}
  numberOfMonths={2}
/>
```

### Progress
**Import:** `@/components/ui/progress`
**Dependencies:** `@radix-ui/react-progress`

```tsx
<Progress value={33} />
<Progress value={66} className="w-[60%]" />
```

### Chart (Recharts)
**Import:** `@/components/ui/chart`
**Dependencies:** `recharts`

```tsx
<ChartContainer config={chartConfig}>
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} tickMargin={10} axisLine={false} />
    <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={8} />
  </BarChart>
</ChartContainer>
```

---

## Feedback Components

### Toast (Radix)
**Import:** `@/components/ui/toast`
**Dependencies:** `@radix-ui/react-toast`

```tsx
// In component
const { toast } = useToast()

toast({
  title: "Scheduled: Catch up",
  description: "Friday, February 10, 2023 at 5:57 PM",
})

toast({
  variant: "destructive",
  title: "Uh oh! Something went wrong.",
  description: "There was a problem with your request.",
})
```

### Sonner (Recommended)
**Import:** `sonner`
**Dependencies:** `sonner`

```tsx
// In layout
import { Toaster } from "@/components/ui/sonner"
<Toaster />

// In component
import { toast } from "sonner"

toast("Event has been created")
toast.success("Event created successfully")
toast.error("Failed to create event")
toast.promise(promise, {
  loading: 'Loading...',
  success: 'Success!',
  error: 'Error!',
})
```

---

## Typography

### Typography Styles
**Import:** `@/components/ui/typography` (custom)

```tsx
// Prose styles for content
<div className="prose prose-slate dark:prose-invert">
  <h1>Heading 1</h1>
  <p>Paragraph text with <a href="#">links</a> and <code>inline code</code>.</p>
  <blockquote>This is a blockquote.</blockquote>
</div>

// Individual elements
<h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
  Heading
</h1>
<p className="leading-7 [&:not(:first-child)]:mt-6">
  Paragraph
</p>
<code className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold">
  Code
</code>
```

---

## Utility Components

### Accordion
**Import:** `@/components/ui/accordion`
**Dependencies:** `@radix-ui/react-accordion`

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Is it accessible?</AccordionTrigger>
    <AccordionContent>
      Yes. It adheres to the WAI-ARIA design pattern.
    </AccordionContent>
  </AccordionItem>
  <AccordionItem value="item-2">
    <AccordionTrigger>Is it styled?</AccordionTrigger>
    <AccordionContent>
      Yes. It comes with default styles that matches the other components.
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

### Kbd (Keyboard)
**Import:** Custom component

```tsx
<kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
  <span className="text-xs">⌘</span>K
</kbd>
```

---

## CSS Variables Reference

Required CSS variables for shadcn/ui theming:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
  }
}
```

---

## Installation (CLI)

```bash
# Initialize shadcn/ui in project
npx shadcn@latest init

# Add individual components
npx shadcn@latest add button
npx shadcn@latest add card dialog
npx shadcn@latest add form input label

# Add all components
npx shadcn@latest add --all
```

---

## Version Compatibility

| Package | Version |
|---------|---------|
| React | ^18.0.0 |
| Next.js | ^14.0.0 (recommended) |
| Tailwind CSS | ^3.4.0 |
| TypeScript | ^5.0.0 |
| class-variance-authority | ^0.7.0 |
| clsx | ^2.0.0 |
| tailwind-merge | ^2.0.0 |
